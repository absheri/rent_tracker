import requests
import datetime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Rent, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Rent

r = requests.get("http://www.thelouisa.com/availableunits.aspx?myOlePropertyId=544239")

p = BeautifulSoup(r.text)

floor_plans = {}

for x in p.find_all(id="other-floorplans"):
    type = x.find_all("h3")[0].text.replace("Floor Plan : ", "").split("-")[0].strip()
    for y in x.parent.parent.parent.next_sibling.find_all("", {"class": "AvailUnitRow"}):
        app_num = y.find("", {"data-label": "Apartment"}).text
        try:
            rent = int(y.find("", {"data-label": "Rent"}).text.strip().replace("$", "").replace(",", "").split("-")[0])
        except:
            rent = 0
        availability = y.find("", {"data-label": "Date Available"}).text
        floor_plans[app_num] = {"rent": rent, "availability": availability, "type": type}

for app_num in floor_plans:
    print(app_num, floor_plans[app_num])

engine = create_engine('sqlite:///rents.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

for app_num in floor_plans:
    r = Rent(date=datetime.datetime.now(), app_number=app_num, rent=floor_plans[app_num]['rent'], availability=floor_plans[app_num]["availability"], type=floor_plans[app_num]["type"])
    session.add(r)
    session.commit()
