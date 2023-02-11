
# %%
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Apple = yf.download("AAPL", start = "2010-01-01", end = "2023-01-01")

# print(Apple)

#Creamos un array con los datos de apertura, cierre, máximo y mínimo
ticker=["AAPL","SPY","MSFT"]
data = yf.download(ticker, start = "2010-01-01", end = "2023-2-08")
#Data.head() mostraria los primeros 5
#


data.to_csv('stocks.csv')

data = pd.read_csv('stocks.csv', parse_dates = True, index_col = 0, header= [0,1] )
data_rounded = round(data,4)
#parse_dates hace que la columna de fechas se convierta en un objeto datetime
#index_col hace que la columna de fechas sea el indice que comienza en 0
#header = [0,1] hace que la primera fila sea el nombre de las columnas y la segunda fila sea el nombre de los subindices

#Our goal is to convert the multi-index to one tuple
data_rounded.columns = data_rounded.columns.to_flat_index()
#to_flat_index() convierte los subindices en una tupla

data_rounded.columns= pd.MultiIndex.from_tuples(data_rounded.columns, names = ['Ticker', 'Stock Info'])
#Convierte la tupla en un multiindex

#print (data_rounded.describe())

#we can store the open or the close for each stock in a 

# %%

close = data_rounded.loc[:,"Close"];
#print (close)

#We are going to draw the close price of each stock
plt.style.use("ggplot")
plt.plot(close)
#This shows the legend of the stocks
plt.legend(close.columns)


##We are going to normalize the data

first = close.iloc[0]   
#iloc[0] toma el primer valor de la columna,
#Si pusieramos ilos[0,0] cogeria el primer valor de la primera columna
close.div(first).mul(100).plot()
print()


# %%
