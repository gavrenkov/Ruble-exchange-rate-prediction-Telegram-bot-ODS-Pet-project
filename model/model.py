import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import tqdm
import datetime


def oli_price_calc(window, oil_price):
    print(window, oil_price)

    base_full_data = pd.read_csv("./model/pet_1.csv", index_col='Date', sep=",", header=0, parse_dates=['Date'])
    base_full_data = base_full_data.sort_index()

    tag_temp = ["Brent_Price"]
    feat_temp = base_full_data[tag_temp].copy()

    m = feat_temp["2020-10-05":"2024-01-01"].index
    feat_temp.loc[m, "Brent_Price"] = [1 / oil_price] * len(m)

    PERIODS = [window]
    AGGREGATES = ["mean"]
    all_features = []

    for period in PERIODS:
        for agg in AGGREGATES:
            rolling_features = feat_temp.rolling(period).aggregate(agg)
            rolling_features.rename(lambda x: "_".join([x, period, agg]), axis=1, inplace=True)
            all_features.append(rolling_features)
    all_features = pd.concat(all_features, axis=1)

    full_data = base_full_data.join(all_features.shift(0, freq="D"))
    full_data = base_full_data[["RUB_Price"]].join(all_features.shift(0, freq="D"))
    full_data = full_data.loc[full_data[:"2022-01-01"].index, :]

    m = full_data["2020-10-05":"2022-01-01"].index
    full_data.loc[m, "RUB_Price"] = [0] * len(m)
    full_data.dropna(how='all', inplace=True)

    tr_data3_1 = full_data["2014-01-01":"2016-12-01"].copy()
    cv_data3_1 = full_data["2016-12-01":].copy()

    # Scaling
    center, scale = tr_data3_1.iloc[:, 1:].mean().values, tr_data3_1.iloc[:, 1:].std().values
    where_are_NaNs = np.isnan(scale)
    scale[where_are_NaNs] = 1
    scale = np.where(scale == 0, 1, scale)
    where_are_NaNs = np.isnan(center)
    center[where_are_NaNs] = 0
    trn3_1 = (tr_data3_1.iloc[:, 1:].fillna(tr_data3_1.iloc[:, 1:].mean()).values - center) / scale
    cvn3_1 = (cv_data3_1.iloc[:, 1:].fillna(tr_data3_1.iloc[:, 1:].mean()).values - center) / scale

    from sklearn.linear_model import Ridge

    # booster="gblinear"
    xgb_model3_1 = Ridge(alpha=0, tol=10e-5)
    xgb_model3_1.fit(trn3_1, (tr_data3_1['RUB_Price'] - tr_data3_1['RUB_Price'].mean()) / tr_data3_1['RUB_Price'].std())

    tr_preds3_1 = xgb_model3_1.predict(trn3_1) * tr_data3_1['RUB_Price'].std() + tr_data3_1['RUB_Price'].mean()
    cv_preds3_1 = xgb_model3_1.predict(cvn3_1) * tr_data3_1['RUB_Price'].std() + tr_data3_1['RUB_Price'].mean()
    tr_preds3_1 = pd.Series(tr_preds3_1.flatten(), index=tr_data3_1.index, name='RUB_Price').sort_index()
    cv_preds3_1 = pd.Series(cv_preds3_1.flatten(), index=cv_data3_1.index, name='RUB_Price')

    plt.figure(figsize=(20, 10))
    #plt.figure(frameon=False)
    (tr_data3_1['RUB_Price']).plot(c="steelblue", label="Real_RUB_Price", fontsize=18)
    (cv_data3_1['RUB_Price']).plot(c="steelblue", label="")
    tr_preds3_1.plot(c="forestgreen", label="train_RUB_Price",fontsize=18)
    cv_preds3_1.plot(c="firebrick", label="test_RUB_Price",fontsize=18)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('RUB/USD', fontsize=18)
    plt.legend(loc=0, fontsize=20)
    plt.xlim([datetime.date(2014, 1, 1), datetime.date(2022, 12, 1)])
    plt.ylim([0, max(max(cv_preds3_1), max(tr_data3_1['RUB_Price'])) + 10])
    # plt.ylim(50,80)
    plt.tight_layout()
    plt.grid()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    plt.title(f'{tr_data3_1.columns[-1]}', fontsize=24)
    plt.savefig('foo.png',bbox_inches='tight', pad_inches=0, dpi=150, quality=100)

    plt.show()
