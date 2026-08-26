from database.database import Base,engine
from database.models import Reservation

Base.metadata.create_all(bind=engine)
print('Reservation table created successfully')