import requests
import time, datetime
import json
from requests_negotiate_sspi import HttpNegotiateAuth
import calendar



# setting target companies

# could find the number of Companies in Anue


configData = [
    {
        "Stock_No": "2355", # 敬鵬 # CHIN POON IND 
        "Code": "C0000001" # Code in Sql 
    },
    {
        "Stock_No": "2383", # 台光電 # ELITE MATL
        "Code": "C0000002" 
    }
    ]



def take_existed_value(config_code_no): 
    url = "http://dataservice/api/CodeEdit/CodeValue"
    params = {
  "code": config_code_no,
  "dataList": [
    {
      "fDate": "",
      "value": ""
    }
  ]
}     
    t_json = requests.get(url,params=params ,headers={'Content-Type':'application/json'},auth=HttpNegotiateAuth())
    data_2 = json.loads(t_json.text)
    return data_2




def connect_tws(num, monthrange):
    url= 'https://marketinfo.api.cnyes.com/mi/api/v1/TWS:' + num + ':STOCK/revenue?months=%s'%(monthrange) # define the lenth of data
                                                                                                           # e.g. monthrange=100, past 100 month revenue data 
    # if proxy is needed
    proxies = dict(http='socks5h://xx.xxx.x.xx:xxxx',
                   https='socks5h://xx.xxx.x.xx:xxxx')
    # otherwise, skip it
    
    try:
        r = requests.get(url, headers = {'Content-Type' : 'application/json',}, 
                        proxies = proxies)
        r_json = r.text
    
    except requests.ConnectionError as e:
        print(e.args)
        
    return r_json


# timeStamp in website and convert it to normal datetime
def ymd_to_ymd(t):
    from datetime import datetime
    parts = t.upper().split('-')
    end = calendar.monthrange(int(parts[0]), int(parts[1]))[1]
    dt = datetime(int(parts[0]), int(parts[1]), end)
    return dt.isoformat()


def timeStamp_2_datatime(stamp):
    otherStyleTime = [datetime.datetime.fromtimestamp(i) for i in stamp]
    DateArray = [i.strftime("%Y-%m-%d %H:%M:%S") for i in otherStyleTime]
    f_Date = [ymd_to_ymd(i) for i in DateArray]    
    return f_Date



def updated_Sql(code,emp):
    url = "http://..."
    salesDate = json.loads(connect_tws(emp))["data"]["time"]
    salesMonth = json.loads(connect_tws(emp))["data"]["datasets"]["saleMonth"]
    # unit adjust
    new_Value = [i*1000 for i in salesMonth][-1]
    f_Date = timeStamp_2_datatime(salesDate)[-1]
    dic = {"fDate": f_Date, "value": new_Value}

    # if there were existing data of this code in Sql, choose the lattest value to compare
    # lattest value in Sql
    t = take_existed_value(code)
    t_value = t[0]["Value"]

    outList = []
    for i in range(0, len(t)):   
        dic2 = {"fDate": t[i]["FDate"], "value": t[i]["Value"]}
        outList.append(dic2)
        

    # Compare the value if there is new value in    
    if salesMonth[-2]*1000 == int(t_value):
        # if the second value got this time equals the lattest value in Sql, then start updating,else pass
        outList.append(dic)
        json_output = {"code": code ,"dataList":outList}    
        data_json = json.dumps(json_output)
        try:
            
            r_json = requests.post(url, data_json,headers={'Content-Type':'application/json'},auth=HttpNegotiateAuth())
            print(Hcode)
            print(f_Date[-1])
            print(r_json)
            print(r_json.text)
            print(r_json.status_code)
            print(r_json.raise_for_status())
            if r_json.status_code == 200:
                print("Insert Successfully!")
                print('-----------------------------------------------------------------------------------')
                
        except:           
            pass
        
    else:
        pass

# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    for i in configData:  
        try:
           updated_Sql(i["Code"],i["Stock_No"])

        except:
           print( i["Code"] + " failed!")














        
