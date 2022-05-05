import configparser
import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def CreateScatterPlot():
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
    
    df.plot(kind='scatter', x = 'year', y = 'earnings')
    plt.xlabel("Year")
    plt.ylabel("Earnings (in millions)")
    plt.title("Earnings by Year")
    plt.savefig('static/images/scatter_plot.png', bbox_inches='tight')