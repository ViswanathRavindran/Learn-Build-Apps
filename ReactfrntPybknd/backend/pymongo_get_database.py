import os
from dotenv import load_dotenv, find_dotenv
import pprint

from pymongo import MongoClient
from pymongo.server_api import ServerApi

load_dotenv(find_dotenv())
password = os.getenv("MONGODB_PWD")

connection_string = f"mongodb+srv://ravindranviswanath:{password}@vishysurvey.ue735.mongodb.net/?retryWrites=true&w=majority&appName=vishysurvey"
printer = pprint.PrettyPrinter()

def get_database():
    # Create a new client and connect to the server
    client = MongoClient(connection_string, server_api=ServerApi('1'))
    # client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        for i in client.list_database_names():
            print(i)

        finaldb = client.vishysurvey
        collections =  finaldb.list_collection_names()
        print("The list of collections are: ", collections)
        print("*********************************************")
        fin_objects = finaldb.vishy_sample.find()
        for i in fin_objects:
            printer.pprint(i)
        print("*********************************************")
        
        fin_objects = finaldb.vishy_sample.find()
        # Extract only the 'name' field
        name_list = [{'name': i['name']} for i in fin_objects if 'name' in i]

        print("The list of dictionaries is: ", name_list)

    except Exception as e:
        print("Failed to ping your deployment. Check your connection")
        print(e)

    return client.vishysurvey

if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database