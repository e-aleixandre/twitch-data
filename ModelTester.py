from classes import Model
import dotenv
from datetime import datetime, timedelta
import os

dotenv.load_dotenv(".env.local")

Model.initialize(os.getenv("DBCON"))

print(Model.get_streamers())
