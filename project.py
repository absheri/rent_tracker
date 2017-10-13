from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Rent, Base
app = Flask(__name__)


engine = create_engine('sqlite:///rents.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/hello')
def all_units():
    rents = session.query(Rent).filter_by()
    grouped = {}
    for x in rents:
        if x.app_number in grouped:
            grouped[x.app_number].append(x)
        else:
            grouped[x.app_number] = [x]

    return render_template('rents.html', grouped=grouped)


@app.route('/rents/<string:app_number>')
def single_unit(app_number):
    rents = session.query(Rent).filter_by(app_number="#"+app_number)
    output = ""
    for x in rents:
        output += x.date.strftime('%Y-%m-%d %H:%M') + " - $" + str(x.rent)
        output += "<br>"
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
