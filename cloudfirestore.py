from bs4 import BeautifulSoup
import requests

URL = "https://www.bursamalaysia.com/market_information/market_statistic/securities"

response = requests.get(URL)
page_content = BeautifulSoup(response.content, "html.parser")

table_body = page_content.find(id="daily_trading_participation")
table = table_body.find("table")
date = table_body.find("p").text

table_rows = table.find_all("tr")[1:]
part_data = {}
for row in table_rows:
    td_symbol = row.find_all('td')[0].text
    td_net = row.find_all('td')[4].text
    td = {}
    td['Participant'] = td_symbol
    td['Net'] = td_net
    part_data[td_symbol] = td_net

#print(part_data)

data = {
    "Date": date,
    "Local Institution Net (RM M)": part_data['Local Institution'],
    "Local Retail Net (RM M)": part_data['Local Retail'],
    "Foreign Net (RM M)": part_data['Foreign']
}

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Singapore')
time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def save(collection_id, document_id, data):
    db.collection(collection_id).document(document_id).set(data)

save(
    collection_id = "Daily Trading Participation",
    document_id = f"{time}",
    data=data
)
