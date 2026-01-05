from database import engine
from database_models import base

print("Dropping all tables...")
base.metadata.drop_all(bind=engine)
print("All tables dropped successfully.")
