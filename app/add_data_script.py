import ijson
from sqlalchemy.orm import sessionmaker

from app.core.db import postgres_engine
from app.phones.models import PhoneData

Session = sessionmaker(bind=postgres_engine)
session = Session()
chunk_size = 1000

with open('/app_back/data.json', 'r') as file:
    parser = ijson.items(file, 'item')
    batch = []
    batch_size = 1000

    for item in parser:
        phone = PhoneData(**item)
        batch.append(phone)
        if len(batch) == batch_size:
            session.add_all(batch)
            batch = []
    if batch:
        session.add_all(batch)
    session.commit()
