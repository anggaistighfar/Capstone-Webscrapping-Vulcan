from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('section',attrs={'class':'box history-rates-table-box'})
table.find_all('div', attrs={'class':'inner'})[:5]
table.find_all('span', attrs={'class':'w'})[:5]
table.find_all('a', attrs={'class':'w'})[:5]
row = table.find_all('a', attrs={'class':'w'})
row_length = len(row)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
    
    #data tanggal
    Date = table.find_all('a', attrs={'class':'n'})[i].text

    #Data harga
    USD_RUPIAH = table.find_all('span', attrs={'class':'w'})[i].text
    USD_RUPIAH = USD_RUPIAH.strip()
 
  
    temp.append((Date,USD_RUPIAH)) 

temp = temp[::-1]

#change into dataframe
data= pd.DataFrame(temp, columns= ('Date', 'USD_RUPIAH'))

#insert data wrangling here
data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
data['USD_RUPIAH'] = data['USD_RUPIAH'].str.extract(r'(\d+,\d+)')[0].str.replace(',','').astype(float)

data =data.set_index('Date')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["USD_RUPIAH"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (10,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)