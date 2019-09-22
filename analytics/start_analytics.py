import pandas as pd

from pyspark.context import SparkContext
from pyspark import SparkConf
from pyspark.sql.session import SparkSession

from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

import matplotlib
import matplotlib.pyplot as plt

coins = ['btc', 'eth']


def arima_train(Actual, P, D, Q):
    model = ARIMA(Actual, order=(P, D, Q))
    model_fit = model.fit(disp=0)
    prediction = model_fit.forecast()[0]
    return prediction


def forecast(actual_data):
    X = actual_data.values
    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()

    print(history)

    # in a for loop, predict values using ARIMA model
    for timepoint in range(len(test)):
        actual_value = test[timepoint]

        prediction = arima_train(history, 5, 1, 0)

        predictions.append(prediction)
        history.append(actual_value)

    # Print MSE to see how good the model is
    error = mean_squared_error(test, predictions)
    print('Test Mean Squared Error: %.3f' % error)


if __name__ == "__main__":
    print("Initializing analytics.")

    conf = SparkConf().set("spark.cassandra.connection.host", "cassandra").setMaster('spark://spark-master:7077')
    sc = SparkContext(conf=conf)
    spark = SparkSession(sc)

    for coin in coins:
        df = spark.read.format("org.apache.spark.sql.cassandra").options(table=coin, keyspace='enigma').load().sort("time")

        pdf = df.toPandas()

        forecast(pdf)
        
        pdf['time'] = pd.to_datetime(pdf['time'], unit='s')
        chart = pdf.plot(kind='line', linestyle="solid", x='time', y='value', colormap='winter_r')

        fig = chart.get_figure()
        fig.savefig(f"./out/{coin}.pdf")

    print("Finished analytics.")
