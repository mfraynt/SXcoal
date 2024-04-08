# SXcoal
Python implementation of API for sxcoal.com

**[SXcoal](https://www.sxcoal.com/en)** is an interactive Chinese information platform dedicated to coal industry. The platform has API, and if you purchase the subscription, they provide you with corresponding documentation. 

Documentation provides user with the detailed description of the API, however it does not contain any particular example of API implementation. This repository contains a quick example of Python code, which can be used to retrieve data from the source.

Present example uses only standard Python libraries. 

API class has only one public method for *Data Request Mode*. Additional methods can be easily added if necessary. 

### Example of usage
```Python
import pandas as pd 
from sxcoal import *

def get_SXcoal_data(dates, templateCode, itemCodes):
    PROXY = {'http': "192.168.1.1", #SPECIFY YOUR PROXY
             'https':  "192.168.1.1"}
    appKey = APPKEY # Replace 'APPKEY' with correspondent value
    appKeySecret = APPKESECRET # Replace 'APPKEYSECRET' with correspondent value
    interface = SX_coal_API(proxy=PROXY, appKey = appKey, appKeySecret = appKeySecret)
    interface.get_data(dates=dates, templateCode=templateCode, itemCodes=itemCodes) # dates in string format, e.g. '20240101-20241231', list template and item codes can be requested from the provider
    response = interface.response
    return response

#EXAMPLE
def generate_initial_data():
    td = datetime.date.today()
    begDate = datetime.date(td.year, 1, 1)
    dates = begDate.strftime("%Y%m%d")+"-"+ td.strftime("%Y%m%d")
    r = get_SXcoal_data(dates=dates,templateCode='P1001I-1', itemCodes="FW1001I-21, FW1001I-26")
    df = pd.json_normalize(r['data']).astype({"dataDate":'datetime64[ns]', "priceUsd":'float64', "priceRmb":'float64'})  
```
