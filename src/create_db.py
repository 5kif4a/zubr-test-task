from src.db import engine
from src.models import Base

Base.metadata.create_all(engine)