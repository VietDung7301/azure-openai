from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

# load env
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")

# connect serve
connection_string = f"mongodb+srv://0606bach:{password}@cluster0.vc1gtc4.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

# export
azure_db = client.AzureOpenAi
collections = azure_db.list_collection_names()
user_vocabularys_collection = azure_db.user_vocabularys
printer = pprint.PrettyPrinter()
