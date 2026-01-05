from database import engine
from fastapi import Depends, FastAPI
from models import Product
from database import session 
import database_models
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
database_models.base.metadata.create_all(bind=engine)


products=[
    Product(id=1,name='MacBook Pro 16"',description='M2 Max, 32GB RAM',category='Electronics',status='In Stock',price=2499.00,quantity=12),
    Product(id=2,name='Logitech MX Master 3S',description='Performance Wireless Mouse',category='Accessories',status='In Stock',price=99.00,quantity=45),
    Product(id=3,name='Samsung Odyssey G9',description='49" Ultra-Wide Gaming Monitor',category='Electronics',status='Low Stock',price=1299.00,quantity=3),
    Product(id=4,name='Herman Miller Aeron',description='Ergonomic Office Chair',category='Furniture',status='Out of Stock',price=1450.00,quantity=0),
    Product(id=5,name='Keychron Q1 Pro',description='Custom Mechanical Keyboard',category='Accessories',status='In Stock',price=199.00,quantity=20),
    Product(id=6,name='Sony WH-1000XM5',description='Noise Canceling Headphones',category='Electronics',status='Low Stock',price=349.00,quantity=8)
]   

def init_db():
    db=session()
    count=db.query(database_models.Product).count()
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db() 

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()    

@app.get('/')
def greet():
    return "Hello World!"

@app.get('/products')
def get_all_products(db:Session=Depends(get_db)):
   db_products=db.query(database_models.Product).all()
   return db_products

@app.get('/product/{id}')
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
       return db_product
    return "Product not found"

@app.post('/product')
def add_product(product:Product,db:Session=Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put('/product/{id}')
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==product.id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.category=product.category
        db_product.status=product.status
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return db_product      
    return "Product not found"

@app.delete('/product/{id}')
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else:
        return "Product not found"    
    