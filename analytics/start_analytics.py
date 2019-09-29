import pandas as pd

from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import normalize, minmax_scale

from cassandra.cluster import Cluster

import matplotlib.pyplot as plt

coins = ['btc', 'eth']


def arima_train(actual, P, D, Q):
    model = ARIMA(actual, order=(P, D, Q))
    model_fit = model.fit(disp=0)
    prediction = model_fit.forecast()[0]
    return prediction


def forecast(actual_data):
    X = actual_data

    size = int(len(X) * 0.66)
    train, test = X[0:size], X[size:len(X)]
    predictions = list()
    actuals = list()
    history = [x for x in train['value']]

    # in a for loop, predict values using ARIMA model
    for timepoint in range(len(test)):
        if timepoint % 2 == 0:
            continue
        actual = test['value'].iloc[timepoint]
        time = test['time'].iloc[timepoint]

        prediction = arima_train(history, 2, 1, 0)[0]
        predictions.append([time, prediction])
        history.append(actual)
        actuals.append([time, actual])

    # Print MSE to see how good the model is
    actuals = pd.DataFrame(data=actuals, columns=['time', 'value'])
    pred = pd.DataFrame(data=predictions, columns=['time', 'value'])

    actuals_scaled = minmax_scale(actuals['value'], feature_range=(0, 1))
    pred_scaled = minmax_scale(pred['value'], feature_range=(0, 1))

    error = mean_squared_error(actuals_scaled, pred_scaled) * 100
    print('Error: %.1f%%' % error)

    return pred, pd.DataFrame(data=train, columns=['time', 'value']), actuals


def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)


def main():
    print("Initializing analytics.")

    cluster = Cluster(contact_points=['cassandra'], port=9042)
    session = cluster.connect('enigma')
    session.row_factory = pandas_factory
    session.default_fetch_size = None

    for coin in coins:
        print(f"Predicting {coin}.")

        res = session.execute(f"SELECT * FROM {coin}", timeout=None)
        d = res._current_rows
        d = d.sort_values(by='time')

        df = d[0:250].copy()

        predictions, training, actual = forecast(df)

        df['time'] = pd.to_datetime(df['time'], unit='s')

        predictions['time'] = pd.to_datetime(predictions['time'], unit='s')
        training['time'] = pd.to_datetime(training['time'], unit='s')
        actual['time'] = pd.to_datetime(actual['time'], unit='s')

        ax = predictions.plot(kind='line', linestyle="solid", x='time', y='value', colormap='Greens_r',
                              label='prediction')
        training.plot(ax=ax, kind='line', linestyle="solid", x='time', y='value', colormap='Blues_r', label='training')
        actual.plot(ax=ax, kind='line', linestyle="solid", x='time', y='value', colormap='Oranges_r', label='actual')

        plt.title('Forecast vs Actuals')
        plt.legend(loc='upper left', fontsize=8)

        print("Done, saving chart.")

        fig = ax.get_figure()
        fig.savefig(f"./out/{coin}.pdf")

        print()

    print("Finished analytics.")


if __name__ == "__main__":
    main()
