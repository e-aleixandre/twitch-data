from classes import Model
import dotenv
from datetime import datetime, timedelta
import os

dotenv.load_dotenv(".env.local")
Model.initialize(os.getenv("DBCON"))
start = datetime.utcnow() - timedelta(days=1)
end = datetime.utcnow()
print(Model.get_scraps(start, end))
print(Model.create_scrap())
print(Model.get_scraps(start, datetime.now()))
Model.close()

