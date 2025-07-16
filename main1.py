from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# GET with path and query params
@app.get("/greet/{name}")
def greet_user(name: str, age: int = 0):
    return {"message": f"Hello {name}, you are {age} years old"}

# POST with request body
class Product(BaseModel):
    name: str
    price: float =101
    in_stock: bool = True

@app.post("/product")
def create_product(product: Product):
    return {"status": "Product created", "product": product}
