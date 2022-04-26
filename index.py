from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import mysql.connector
import configparser
import csv

Base = declarative_base()

app = Flask(__name__)

class Athletes(Base):
    __tablename__ = 'richathletes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    currentrank = Column(Integer, nullable=False)
    prevyearrank = Column(Integer, nullable=True)
    sport = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    earnings = Column(Float, nullable=False)

    def __repr__(self):
        return "<Athletes(id = '%s', name='%s', nationality='%s', currentrank='%s', prevyearrank='%s', sport='%s', year='%s', earnings='%s')>" % (self.id, self.name, self.nationality, self.currentrank, self.prevyearrank, self.sport, self.year, self.earnings)

bootstrap = Bootstrap(app)

@app.before_first_request
def ReadCSV():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    
    mydb = mysql.connector.connect(
        host = config['MYSQL']['HOSTNAME'],
        user = config['MYSQL']['USERNAME'],
        password = config['MYSQL']['PASSWORD'],
        database = 'richathletes'
    )

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("""truncate table athletes""")

    with open('data/richathletes.csv', 'r') as athletes:
        csv_reader = csv.reader(athletes, delimiter=',')

        next(csv_reader)

        for row in csv_reader:
            mycursor.execute("""INSERT INTO athletes (name, nationality, currentrank, prevyearrank, sport, year, earnings) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)""", row)
    
    mydb.commit()
    mycursor.close()

@app.route('/')
def index():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    
    mydb = mysql.connector.connect(
        host = config['MYSQL']['HOSTNAME'],
        user = config['MYSQL']['USERNAME'],
        password = config['MYSQL']['PASSWORD'],
        database = 'richathletes'
    )
    
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("""SELECT year, name, earnings FROM athletes 
    WHERE currentrank = 1""")
    athletes = mycursor.fetchall()

    return render_template('database.html', athletes=athletes)

@app.route('/page1')
def page1():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    
    mydb = mysql.connector.connect(
        host = config['MYSQL']['HOSTNAME'],
        user = config['MYSQL']['USERNAME'],
        password = config['MYSQL']['PASSWORD'],
        database = 'richathletes'
    )

    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("""SELECT year, name, nationality, prevyearrank FROM athletes 
    WHERE currentrank = 1 AND year > 1990""")
    athletes = mycursor.fetchall()

    return render_template('page1.html', athletes=athletes)

@app.route('/page2')
def page2():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    
    mydb = mysql.connector.connect(
        host = config['MYSQL']['HOSTNAME'],
        user = config['MYSQL']['USERNAME'],
        password = config['MYSQL']['PASSWORD'],
        database = 'richathletes'
    )

    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("""SELECT year, ROUND(sum(earnings)/10, 2) as combined_earnings_per_year, 
    name FROM athletes GROUP BY year""")
    athletes = mycursor.fetchall()

    return render_template('page2.html', athletes=athletes)

@app.route('/page3')
def page3():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    
    mydb = mysql.connector.connect(
        host = config['MYSQL']['HOSTNAME'],
        user = config['MYSQL']['USERNAME'],
        password = config['MYSQL']['PASSWORD'],
        database = 'richathletes'
    )

    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("""SELECT sport, MAX(earnings) as highest_earnings, 
    MIN(earnings) as lowest_earnings, MAX(earnings) - MIN(earnings) as range_of_earnings 
    FROM athletes GROUP BY sport ORDER BY range_of_earnings desc""")
    athletes = mycursor.fetchall()

    return render_template('page3.html', athletes=athletes)

if __name__ == '__main__':
    app.run(debug=True)