import crab
import time
import datetime
import numpy as np

City = ['Beijing','Shanghai','Xiamen','Guangzhou','Chengdu','Shenzhen','Xian','Nanjing','Hangzhou',
        'Chongqing','Wuhan','Suzhou','Wuxi','Qingdao','Sanya','Dalian','Haerbin','Kunming','Xianggang',
        'Shenyang','Zhengzhou']
CityId = [12,13,76,16,45,17,176,65,26,15,194,67,66,114,144,56,93,225,344,55,103]

assert len(City) == len(CityId)

def urlProvidor(luId):
    timestamp =  time.mktime(time.localtime())*1000
    url = 'http://wireless.xiaozhu.com/app/xzfk/html5/201/detail/index?' \
          'jsonp=detailindex_callback&luId=%d&startDate=' \
          '&endDate=&userId=0&sessId=0&jsonp=detailindex_callback'%luId
    return url


# for string issues
true = True
false = False
null = ''
#end string issues

#fetch unique luId from DB
query = {}
query['luId']={
    'luId':'group by',
    # 'cityId': 'where (cityId = 12 or cityId = 13 or cityId = 144)',
}
query_old = {}
query_old['houseInfo']={
    'luId':'group by',
    # 'cityId': 'where (cityId = 12 or cityId = 13 or cityId = 144)',
}
cols, rows = crab.database.db(query,'select')
cols_old, rows_old = crab.database.db(query_old,'select')
if cols == cols_old:
    rows = [i for i in rows if i not in rows_old]
#end fetch unique luId from DB
print 'updating %d new houseInfo'%len(rows)

for row in rows:
    try:
        luId = row[cols.index('luId')]
        format = crab.formator.formator('"content":{.+}\)')
        rawData = crab.locator.locator(urlProvidor(luId),format)

        if len(rawData) == 1:
            rawData = rawData[0]
            content = rawData[10:-2]
            content = eval(content)
        else:
            print 'passed luId : %d'%luId
            continue
        keys = ['luId','landlordId','lodgeUnitName','yanzhen','shipai','isFlashBook','isNew','online','leaseType',
                'area','houseType','guestNum','liveTips','displayAddress','latitude','longitude','roomInnerIntro','serviceIntro',
                'trafficIntro','toilet','foreigner','maxDays','minDays','addPriceDesc','cashPlege','cashPledgeOnline',
                'cashPlegeFree','aroundVillageIntro','sheetChange','addTenant','addTenantTips','bedInfo','bedNum','bedNumTip',
                'wirelessnetwork','shower','tv','aircondition','heater','smoke','drinking','slippers','toiletpaper',
                'towel','toiletries','icebox','washer','elevator','iscook','accesssys','parkingspace','wirednetwork',
                'brush','soap','botbathtub','pet','meet','useRule','unReceiveSex','unReceiveAge','cancelPayAllDay',
                'prepayRate','cancelPunishDay','city_id','updateTime']
        json = {}
        if isinstance(content, dict):
            for key,value in content.iteritems():
                if isinstance(value,dict):
                    for valuekey,valuevalue in value.iteritems():
                        if valuekey in keys:
                            if not isinstance(valuevalue,list):
                                json[valuekey]=valuevalue
                            else:
                                json[valuekey]=','.join(valuevalue)
                elif (key in keys) and (not isinstance(value,list)):
                    json[key] = value
        if isinstance(content['facility'],list):
            for item in content['facility']:
                if item['key'] in keys:
                    json[item['key']] = item['display']
        json['luId'] = luId
        json['searchTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        change = {
            'houseInfo' : json,
        }

        crab.database.db(change,'insert')

        json = {}
        json['luId'] = luId
        json['searchTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json['promotionWeek'] = content['priceAndTips']['promotionWeek']
        json['promotionMonth'] =content['priceAndTips']['promotionMonth']
        json['isTejia'] =content['priceAndTips']['isTejia']
        json['displayPrice'] = content['priceAndTips']['displayPrice']

        crab.database.db({'promotion':json},'insert')

    except KeyboardInterrupt:
        exit()
    except:
        try:
            errorHandler = {}
            errorHandler['url'] = urlProvidor(luId)
            errorHandler['description'] = 'houseInfo'
            errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            crab.database.db({'errorHandler':errorHandler},'insert')
        except:
            print 'passed luId %d with no DB errorHandler record'%luId
# except Exception as inst:
#     errorHandler = {}
#     errorHandler['url'] = urlProvidor(city,minprice,minprice+dprice)
#     errorHandler['description'] = inst.message
#     errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print 'error result in price : %d - %d '%(minprice,minprice+dprice)





if __name__ == 'main':
    pass
