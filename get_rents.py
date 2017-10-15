import requests
import datetime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Apartment, Rent, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Rent

r = requests.get("http://www.thelouisa.com/availableunits.aspx?myOlePropertyId=544239")

p = BeautifulSoup(r.text)

floor_plans = {}

for x in p.find_all(id="other-floorplans"):
    type = x.find_all("h3")[0].text.replace("Floor Plan : ", "").split("-")[0].strip()
    path_to_floor_plan = "http://cdngeneral.rentcafe.com/" + x.parent.find_all("", {"href": "javascript:void(0);"})[0].attrs["onmouseout"].split(",")[3].strip().replace("'", "").replace("width=350", "")
    for y in x.parent.parent.parent.next_sibling.find_all("", {"class": "AvailUnitRow"}):
        app_num = y.find("", {"data-label": "Apartment"}).text
        try:
            rent = int(y.find("", {"data-label": "Rent"}).text.strip().replace("$", "").replace(",", "").split("-")[0])
        except:
            rent = 0
        availability = y.find("", {"data-label": "Date Available"}).text

        floor_plans[app_num] = {"path_to_floor_plan": path_to_floor_plan,
                                "rent": rent,
                                "availability": availability,
                                "type": type}

for app_num in floor_plans:
    print(app_num, floor_plans[app_num])

engine = create_engine('sqlite:///rents.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

for app_num in floor_plans:

    db_apartment = session.query(Apartment).filter_by(app_number=app_num).first()

    if not db_apartment:
        db_apartment = Apartment(app_number=app_num,
                                 path_to_floor_plan=floor_plans[app_num]["path_to_floor_plan"],
                                 availability=floor_plans[app_num]["availability"],
                                 type=floor_plans[app_num]["type"])
        session.add(db_apartment)
        session.commit()

    r = Rent(date=datetime.datetime.now(),
             rent=floor_plans[app_num]['rent'],
             apartment_id=db_apartment.id,
             Apartment=db_apartment)

    session.add(r)
    session.commit()
