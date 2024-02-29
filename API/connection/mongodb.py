from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongoUri = os.getenv('MONGODB_URI')

client = MongoClient(mongoUri)