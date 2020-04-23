import logging

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_REMOTE_URL, WEATHERBIT_API_KEY
from models.models import Miasto, PogodaHistoria
from utils.weather_api import WeatherBitIo
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

logging.info('I am creating a engine')
engine = create_engine(DATABASE_REMOTE_URL)
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

logging.info('I am creating a session')
# Find All cities with czy_prognoza = True flag in iterate

pogoda_historia = session.query(PogodaHistoria).order_by(PogodaHistoria.id_pogoda_h.asc())[-50:]

for prognoza in pogoda_historia:
    logging.info([prognoza.id_pogoda_h ,prognoza.czas_pogoda_h, prognoza.temp_zewn_h, prognoza.id_miasto, session.query(Miasto).get(prognoza.id_miasto).miasto_nazwa ])
# Commit changes in db
session.commit()
logging.info('Finished')
# Close session
connection.close()
# Close engine connection
engine.dispose()
