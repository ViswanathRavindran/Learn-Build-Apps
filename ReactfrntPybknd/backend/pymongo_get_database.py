from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ravindranviswanath:vishy135@vishysurvey.ue735.mongodb.net/?retryWrites=true&w=majority&appName=vishysurvey"

def get_database():
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # client = MongoClient(uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        for i in client.list_database_names():
            print(i)

    except Exception as e:
        print("Failed to ping your deployment. Check your connection")
        print(e)

    return client['vishysurvey']

if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()

    