import uvicorn
from fastapi import FastAPI, send_from_directory
from fastapi.middleware.cors import CORSMiddleware
from pymongo_get_database import get_database
from pydantic import BaseModel
from typing import List
import os

class Fruit(BaseModel):
    name: str

class Fruits(BaseModel):
    fruits: List[Fruit]

app = FastAPI()

origins = [
    "http://localhost:5173"
    # "https://netlify.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# memory_db = {"fruits" : []}

dbname = get_database()
collection_name = dbname.vishy_sample
print("DB Connection Successful", collection_name)

def insert_test_doc():
    collection = dbname.vishy_sample
    item_1 = {
                "name" : "water melon",
                }
    inserted_id = collection.insert_one(item_1)
    print("Inserted ID: ", inserted_id.inserted_id)

# insert_test_doc()
# collection_name.insert_many([item_1,item_2])

@app.get("/fruits", response_model=Fruits)
def get_fruits():
    # print("this is the structure of the data inside db: ", memory_db["fruits"])
    fin_objects = dbname.vishy_sample.find()
    # Extract only the 'name' field
    name_list = [{'name': i['name']} for i in fin_objects if 'name' in i]
    print("The list of dictionaries is: ", name_list)

    #Add the fruits dictionary for name_list
    fruits = {"fruits":name_list}
    print("The fruits dictionary is: ", fruits)
    return fruits
    # return Fruits(fruits=memory_db["fruits"])

@app.post("/fruits", response_model=Fruit)
def add_fruit(fruit: Fruit):
    print("this is the structure of the input: ", fruit)
    # convert name='new fruit' to {'name':'new fruit'}
    fruit_dict = fruit.dict()
    print("this is the structure of the input: ", fruit_dict)

    # memory_db["fruits"].append(fruit)
    collection = dbname.vishy_sample
    collection.insert_one(fruit_dict)
    return fruit_dict

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)