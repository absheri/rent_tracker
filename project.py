from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Apartment, Rent, Base
import datetime
app = Flask(__name__)


engine = create_engine('sqlite:///rents.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def all_units():
    aparts = session.query(Apartment).filter_by()
    grouped = []
    for x in aparts:
        rents = session.query(Rent).filter_by(apartment_id=x.id)
        grouped.append((x, rents))

    return render_template('rents.html', grouped=grouped, two_days_ago=datetime.datetime.now()-datetime.timedelta(days=2))


@app.route('/rents/<string:apartment_id>')
def single_unit(apartment_id):
    rents = session.query(Rent).filter_by(apartment_id=apartment_id)
    output = ""
    for x in rents:
        output += x.date.strftime('%Y-%m-%d %H:%M') + " - $" + str(x.rent)
        output += "<br>"
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
