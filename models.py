from pydantic import BaseModel
class Product(BaseModel):
    id:int
    name:str
    description:str
    category:str
    status:str
    price:float
    quantity:int
    
   