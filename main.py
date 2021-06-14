import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_historic_price(symbol, exchange='bitfinex', after='2021-06-05'):
    url = 'https://api.cryptowat.ch/markets/{exchange}/{symbol}usd/ohlc'.format(
        symbol=symbol, exchange=exchange)
    resp = requests.get(url, params={
        'periods': '86400',
        'after': str(int(pd.Timestamp(after).timestamp()))
    })
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(data['result']['86400'], columns=[
        'CloseTime', 'OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice', 'Volume', 'NA'
    ])
    df['CloseTime'] = pd.to_datetime(df['CloseTime'], unit='s')
    df.set_index('CloseTime', inplace=False)
    print(df)
    return df


last_week = (pd.Timestamp.now() - pd.offsets.Day(7))
btc = get_historic_price('btc', 'kraken', after=last_week)
eth = get_historic_price('eth', 'kraken', after=last_week)
plt.title('7-Day Coin Price')
print(btc['ClosePrice'].describe())

plt.subplot(2, 1, 1)
btc['ClosePrice'].plot(figsize=(20, 12))
plt.title('7-Day Coin Price')
plt.ylabel('Price')
plt.legend(['Bitcoin', ''])

plt.subplot(2, 1, 2)
eth['ClosePrice'].plot(figsize=(20, 12))
plt.legend(['Ethereum', ''])
plt.ylabel('Price')
plt.savefig('7-Day Coin Price.png')

plt.figure(figsize=(14, 9))
plt.bar(btc['CloseTime'], btc['ClosePrice'], color='#FFD700', width=0.5)
plt.bar(eth['CloseTime'], eth['ClosePrice'], color='#FFA500', width=0.5)
plt.legend(['Bitcoin Volume', 'Ethereum Volume'])
plt.title('Liquidity')
plt.savefig('Liquidity')
