import time
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stockstats import StockDataFrame

pd.options.mode.chained_assignment = None  # default='warn'
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize']=(20,10)
pd.set_option("display.max_rows",20,'display.max_columns', None)


def get_historical_data(sembol, bas_tar):
    api_key = 'd049416976914901aa4255600bd4ed53'
    api_url = f'https://api.twelvedata.com/time_series?symbol={sembol}&interval=1day&outputsize=5000&apikey={api_key}'
    raw_df=requests.get(api_url).json()
    df=pd.DataFrame(raw_df['values']).iloc[::-1].set_index('datetime').astype(float)
    df=df[df.index >= bas_tar]
    df.index=pd.to_datetime(df.index)
    return df

aaa=get_historical_data('XRP/USD','2021-10-27')
k= StockDataFrame(aaa)
x=np.arange(0,len(k),1)
y=k.close
plt.plot(x,y)
der=1
max=0
maxm=0
maxn=0
maxtt=0
maxder=0
maxMer=1
for mer in range(1,3):
    for tt in range(10,20,1):
        for m in np.arange(0,10,1):
            for n in np.arange(-10,0,1):
                top=1000
                lot=0
                Al=0
                Sat=1
                for i in range(tt,len(y)):
                    katsayilar = np.polyfit(x[i-tt:i],y[i-tt:i],mer)
                    if(round(1000*katsayilar[0],der)>m and Al==0):
                        Al=1
                        Sat=0
                        lot=round(top/y[i])
                        top=top-lot*y[i]
                        # plt.plot.(x[i],y[i],'g^')
                    elif(round(1000*katsayilar[0],der)<n and Sat==0):
                        Al=0
                        Sat=1
                        top=top+lot*y[i]
                        lot=0
                        #plt.plot(x[i]iy[i],'rv')

                if(top+lot*y[-1]>max):
                    max=top+lot*y[-1]
                    maxm=m
                    maxn=n
                    maxtt=tt
                    maxder=der
                    maxMer=mer
                    print("Tahmini kazanc={0:.1f} katsayilar={1} {2} {3} derece={4} mertebe={5}".format(max,m,n,tt,der,mer))



top = 1000
lot = 0
Al = 0
Sat = 1
for i in range(maxtt,len(k)):
    katsayilar = np.polyfit(x[i-maxtt:i], y[i-maxtt:i], maxMer)
    if (round(1000 * katsayilar[0], maxder) > maxm and Al == 0):
        Al = 1
        Sat = 0
        lot = round(top / y[i])
        top = top - lot * y[i]
        plt.plot(x[i],y[i],'g^')
    elif (round(1000 * katsayilar[0], maxder) < maxn and Sat == 0):
        Al = 0
        Sat = 1
        top = top +lot* y[i]
        lot = 0
        plt.plot(x[i],y[i],'rv')
print("Gercek kazanc={0:.1f}".format(top+lot*y[-1]))

plt.show()
