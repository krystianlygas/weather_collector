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
cities = session.query(Miasto).filter_by(czy_prognoza=True)
nb_of_cities = cities.count()
for nb, city in enumerate(cities, 1):

    # IT will be better to change id_pogoda_h to SERIAL for autoincrement primary key
    next_id = session.query(PogodaHistoria).order_by(
        PogodaHistoria.id_pogoda_h.desc()).first().id_pogoda_h + 1

    # Instance of the WeatherBitIo Class, for gps localisation from city object
    weather_api = WeatherBitIo(
        lat=city.gps_latitude, lon=city.gps_longitude, apikey=WEATHERBIT_API_KEY)

    # Get current weather data for city
    current_weather = weather_api.get_current_weather()

    # Create new PogodaHistoria object (ORM), with the current_weather data
    pogoda_historia = PogodaHistoria(id_pogoda_h=next_id, temp_zewn_h=current_weather['temp'], wiatr_predkosc_h=current_weather['wind_spd'], wiatr_kierunek_h=current_weather['wind_dir'],
                                     zachmurzenie_h=current_weather['clouds'], naslonecznienie_calk_h=current_weather[
                                         'ghi'], id_miasto=city.id_miasto, czas_pogoda_h=current_weather['datetime'],
                                     naslonecznienie_rozpr_h=current_weather['dhi'], naslonecznienie_bezpn_h=current_weather[
                                         'dni'], naslonecznienie_szac_h=current_weather['solar_rad'],
                                     wilgotnosc_wzgl_h=current_weather['rh'], temp_odczuw_h=current_weather['app_temp'])
    # Add record to db
    session.add(pogoda_historia)

    logging.info(f'Progress: {nb/nb_of_cities*100}%')
# Commit changes in db
session.commit()
logging.info('Finished')
# Close session
connection.close()
# Close engine connection
engine.dispose()
