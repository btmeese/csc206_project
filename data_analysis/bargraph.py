import configparser
import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def CreateBarGraph():
    config = configparser.ConfigParser()
    config.read('settings.conf')
    
    mydb = mysql.connector.connect(
        host = config['MYSQL']['HOSTNAME'],
        user = config['MYSQL']['USERNAME'],
        password = config['MYSQL']['PASSWORD'],
        database = 'richathletes'
    )

    query = "SELECT nationality FROM athletes WHERE currentrank = 1"
    df = pd.read_sql(query, mydb)

    df.groupby('nationality').size().plot(kind='bar')
    plt.xticks(rotation=70)
    plt.xlabel("Nationality")
    plt.ylabel("Number of Athletes")
    plt.ylim(0, 30)
    plt.title("Number of Highest Earning Athletes Per Nationality")
    plt.savefig('static/images/bar_graph.png', bbox_inches='tight')