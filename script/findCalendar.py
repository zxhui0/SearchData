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
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    endDate= (datetime.datetime.now()+datetime.timedelta(120,0)).strftime("%Y-%m-%d")


    url = 'http://wireless.xiaozhu.com/app/xzfk/html5/201/detail/Cal?jsonp=' \
        'detail_cal_callback&luId={}&startDate={}&endDate={}&' \
        'userId=0&sessId=0&jsonp=detail_cal_callback&' \
        'timestamp={}&_={}'.format(
        luId,today,endDate,timestamp,timestamp+200
    )
    return url




# for string issues
true = True
false = False
null = ''
#end string issues

#fetch unique landlordId from DB
query = {}
query['houseInfo']={
    'luId' : 'group by',
}
cols, rows = crab.database.db(query,'select')
#end fetch unique landlordId from DB
# #fetch exist landlordId from DB
# query = {}
# query['landlordInfo']={
#     'luId' : 'group by',
# }
# existCols, existRows = crab.database.db(query,'select')
# #end fetch exist landlordId from Db

luIds = [i[cols.index('luId')] for i in rows]

# existLandlordIds = [i[existCols.index('landlordId')] for i in existRows]
# newLandlordIds = [i for i in landlordIds if not i in existLandlordIds]


print 'searching %d luIds for priceCalendar'%len(luIds)
json={}
json['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json['activity'] = 'searchCalendar'
json['status'] = 'starting'
try:
    crab.database.db({'activityRecord':json},'insert')
except:
    pass

for luId in np.random.permutation(luIds):
    try:
        format = crab.formator.formator('"content":\[{.+\]}\)')
        rawData = crab.locator.locator(urlProvidor(luId),format)

        if len(rawData) == 1:
            rawData = rawData[0]
            content = rawData[10:-2]
            content = eval(content)
        else:
            print 'passed luId : %d'%luId
            continue
        for item in content:

            keys = ['luId','searchTime','Day','price','userSetBookable','isCanBook','priceType','roomNum']
            json = {}
            if isinstance(item, dict):
                for key,value in item.iteritems():
                    if isinstance(value,dict):
                        for valuekey,valuevalue in value.iteritems():
                            if valuekey in keys:
                                if not isinstance(valuevalue,list):
                                    json[valuekey]=valuevalue
                                else:
                                    json[valuekey]=','.join(valuevalue)
                    elif (key in keys) and (not isinstance(value,list)):
                        json[key] = value
            json['luId'] = luId
            json['Day']=item['day']
            json['searchTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if json['isCanBook'] == False:
                change = {
                    'priceCalendar' : json,
                }
                crab.database.db(change,'insert')

    except KeyboardInterrupt:
        exit()
    except:
        try:
            errorHandler = {}
            errorHandler['url'] = urlProvidor(landlordId)
            errorHandler['description'] = 'failed insert priceCalendar data of luId : %d'%luId
            errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            crab.database.db({'errorHandler':errorHandler},'insert')
        except:
            print 'passed luId %d with no DB errorHandler record'%luId


json={}
json['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json['activity'] = 'searchCalendar'
json['status'] = 'finished'
try:
    crab.database.db({'activityRecord':json},'insert')
except:
    pass

# except Exception as inst:
#     errorHandler = {}
#     errorHandler['url'] = urlProvidor(city,minprice,minprice+dprice)
#     errorHandler['description'] = inst.message
#     errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print 'error result in price : %d - %d '%(minprice,minprice+dprice)





if __name__ == 'main':
    pass
