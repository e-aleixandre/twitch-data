from classes import MongoScrapeModel, DataProcessor, MariaDBReportsModel
import dotenv
import os
from datetime import datetime
from time import time
from memory_profiler import memory_usage
import logging
import sys

# Time calculation variables
starting_time = time()
dbcon_time = 0
dbfetch_time = 0
instantiation_time = 0
export_time = 0

# Setting CWD because cronjob uses home by default
cwd = os.path.dirname(__file__)
if cwd != '':
    os.chdir(cwd)

starting_time = time()

# LOADING ENV VARIABLES
dotenv.load_dotenv(".env.local")

# Initializing
logging.basicConfig(filename=os.getenv("LOGS") + "/exporter.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Exporter started.")

try:
    min_date = datetime.strptime(sys.argv[1], "%Y-%m-%dT%H:%M")
    max_date = datetime.strptime(sys.argv[2], "%Y-%m-%dT%H:%M")
    report_id = int(sys.argv[3])
except Exception as e:
    logging.critical("An error occurred while parsing the dates. Logging the exception.")
    logging.exception(e)
    exit(-1)

try:
    scrape_model = MongoScrapeModel.MongoScrapeModel(os.getenv("DBCON"), os.getenv("DB"))
    reports_model = MariaDBReportsModel.MariaDBReportsModel(os.getenv("FRONTENDDB_USER"), os.getenv("FRONTENDDB_PASS"), os.getenv("FRONTENDDB_HOST"), os.getenv("FRONTENDDB_NAME"))
    dbcon_time = time()
    logging.info("DBs connection time: %s" % (dbcon_time - starting_time))
except Exception as e:
    logging.critical("An error occurred connecting to the database. Logging the exception.")
    logging.exception(e)
    exit(-1)

try:
    pid = os.getpid()
    reports_model.set_pid(report_id, pid)
except Exception as e:
    logging.critical("An error occurred while updating the pid. Logging the exception.")
    logging.exception(e)
    reports_model.set_errored(report_id)  # Could give an error as well...
    exit(-1)

try:
    scrapes_list = scrape_model.get_scrapes(min_date, max_date)
    dbfetch_time = time()
    logging.info("Memory usage after get_scrapes: %s" % memory_usage())
    logging.info("Scrapes fetch time: %s" % (dbfetch_time - dbcon_time))
except Exception as e:
    logging.critical("An error occurred while fetching the database. Logging the exception.")
    logging.exception(e)
    reports_model.set_errored(report_id)

    exit(-1)

if not scrapes_list:
    logging.warning("No data. This could be caused by an undetected error.")
    logging.warning("Min date: %s\tMax date: %s" % (min_date, max_date))
    reports_model.set_errored(report_id)

    exit(0)

try:
    logging.info("Processing the data.")
    processor = DataProcessor.DataProcessor(scrapes_list, min_date, max_date, os.getenv("EXPORTS"))
    instantiation_time = time()
    logging.info("Memory usage after instantiating the DataProcessor: %s" % memory_usage())
    logging.info("Time to instantiate DataProcessor: %s" % (instantiation_time - dbfetch_time))

except Exception as e:
    logging.critical("An error raised while processing the data. Logging the exception.")
    logging.exception(e)
    reports_model.set_errored(report_id)
    exit(-1)

try:
    logging.info("Exporting the data.")
    response = processor.export()
    export_time = time()
    logging.info("Exporting time: %s" % (export_time - instantiation_time))
    reports_model.set_completed(report_id, response)
except Exception as e:
    logging.error("Error while exporting the data. Logging the exception.")
    logging.exception(e)
    reports_model.set_errored(report_id)
finally:
    reports_model.close()
