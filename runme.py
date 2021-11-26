import threading
from requests import api
import schedule
import time, json
import requests

apiKey = "2Y8QU5VNJ6FV89FG2F6MQ8QYRIUNKUKY29"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# m_url = "http://127.0.0.1:8000"
m_url = "https://ravenftmarket.net/"

def check_for_approval():
    p = requests.get(m_url+'/applied_for_purchasing')
    applied_for_purchasing = json.loads(p.json())
    for i in applied_for_purchasing:
        txhash = i['fields']['transaction_id']
        print(txhash)
        p = requests.get(
            "https://api.bscscan.com/api?module=transaction&action=gettxreceiptstatus&txhash={}&apikey={}".format(txhash, apiKey))
        # Test one : 
        # p = requests.get("https://api-testnet.bscscan.com/api?module=transaction&action=gettxreceiptstatus&txhash={}&apikey={}".format(txhash, apiKey), headers=headers)
        if(p.json()['result']['status'] == "1"):
            p = requests.get(m_url+'/purchased/'+i['pk'])
            print(p.text)
        else:
            print("Nope")

def run_checking(job_func):
    th = threading.Thread(target=job_func)
    th.start()

# check_for_approval()
schedule.every(2).minutes.do(run_checking, check_for_approval)

while True:
    schedule.run_pending()
    time.sleep(1)
