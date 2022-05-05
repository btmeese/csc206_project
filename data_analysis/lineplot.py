import configparser
import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def CreateLinePlot():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    
    mydb = mysql.connector.connect(
        host = config['MYSQL']['HOSTNAME'],
        user = config['MYSQL']['USERNAME'],
        password = config['MYSQL']['PASSWORD'],
        database = 'richathletes'
    )

    query = "SELECT * FROM athletes"
    df = pd.read_sql(query, mydb)
    
    df.groupby('year').agg({'earnings':'median'}).plot()
    plt.xlabel("Year")
    plt.ylabel("Median Earnings (in millions)")
    plt.title("Median Earnings by Year")
    plt.savefig('static/images/line_plot.png', bbox_inches='tight')