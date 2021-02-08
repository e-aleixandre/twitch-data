from classes import Model, DataProcessor
import dotenv
import os
from datetime import datetime
import logging
import sys
import json

# Setting CWD because cronjob uses home by default
os.chdir(os.path.dirname(__file__))

# LOADING ENV VARIABLES
dotenv.load_dotenv(".env.local")

# Initializing
logging.basicConfig(filename=os.getenv("LOGS") + "/exporter.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Exporter started.")

min_date = datetime.strptime(sys.argv[1], "%Y-%m-%dT%H:%M")
max_date = datetime.strptime(sys.argv[2], "%Y-%m-%dT%H:%M")

try:
    Model.initialize(os.getenv("DBCON"))
except Exception as e:
    logging.critical("An error occurred connecting to the database. Logging the exception.")
    logging.exception(e)
    results = {
        "ok": False,
        "code": 1
    }

    sys.stdout.write(json.dumps(results))
    exit(-1)

try:
    scraps_list = Model.get_scraps(min_date, max_date)
except Exception as e:
    logging.critical("An error occurred while fetching the database. Logging the exception.")
    logging.exception(e)

    results = {
        "ok": False,
        "code": 2
    }

    sys.stdout.write(json.dumps(results))
    exit(-1)

if not scraps_list:
    logging.warning("No data. This could be caused by an undetected error.")
    logging.warning("Min date: %s\tMax date: %s" % (min_date, max_date))

    results = {
        "ok": False,
        "code": 10
    }

    sys.stdout.write(json.dumps(results))
    exit(0)

try:
    logging.info("Processing the data.")
    processor = DataProcessor.DataProcessor(scraps_list, min_date, max_date, os.getenv("EXPORTS"))
except Exception as e:
    logging.critical("An error raised while processing the data. Logging the exception.")
    logging.exception(e)
    results = {
        "ok": False,
        "code": 3
    }

    sys.stdout.write(json.dumps(results))
    exit(-1)

try:
    logging.info("Exporting the data.")
    response = processor.export()
    results = {
        "ok": True,
        "fileName": response
    }

    sys.stdout.write(json.dumps(results))
except Exception as e:
    logging.error("Error while exporting the data. Logging the exception.")
    logging.exception(e)
    results = {
        "ok": False,
        "code": 20
    }

    sys.stdout.write(json.dumps(results))
