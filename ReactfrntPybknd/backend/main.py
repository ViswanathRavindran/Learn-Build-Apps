import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo_get_database import get_database
from pydantic import BaseModel
from typing import List

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

memory_db = {"fruits" : []}

dbname = get_database()
collection_name = dbname.vishy_sample
print("DB Connection Successful", collection_name)

def insert_test_doc():
    collection = dbname.vishy_sample
    item_1 = {
                "name" : "plum"
                }
    inserted_id = collection.insert_one(item_1)
    print("Inserted ID: ", inserted_id.inserted_id)

insert_test_doc()
# collection_name.insert_many([item_1,item_2])

@app.get("/fruits", response_model=Fruits)
def get_fruits():
    print("this is the structure of the data inside db: ", memory_db["fruits"])
    return Fruits(fruits=memory_db["fruits"])
    # return Fruits(fruits=collection_name.find())

@app.post("/fruits", response_model=Fruit)
def add_fruit(fruit: Fruit):
    print("this is the structure of the input: ", fruit)
    memory_db["fruits"].append(fruit)
    # collection_name.insert_one(fruit)
    return fruit

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)