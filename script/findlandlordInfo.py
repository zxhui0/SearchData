import crab
import time
import datetime
import numpy as np

City = ['Beijing','Shanghai','Xiamen','Guangzhou','Chengdu','Shenzhen','Xian','Nanjing','Hangzhou',
        'Chongqing','Wuhan','Suzhou','Wuxi','Qingdao','Sanya','Dalian','Haerbin','Kunming','Xianggang',
        'Shenyang','Zhengzhou']
CityId = [12,13,76,16,45,17,176,65,26,15,194,67,66,114,144,56,93,225,344,55,103]

assert len(City) == len(CityId)

def urlProvidor(landlordId):
    timestamp =  time.mktime(time.localtime())*1000
    url = 'http://wireless.xiaozhu.com/app/xzfk/html5/201/Fangdong/index?' \
          'jsonp=fangdongindex_callback&landlordId={}&offset=0&' \
          'length=5&onlyLodgeunit=false&userId=0&sessId=0&' \
          'jsonp=fangdongindex_callback&timestamp={}&_={}'.format(
        landlordId,timestamp,timestamp+200
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
    'landlordId' : 'group by',
}
cols, rows = crab.database.db(query,'select')
#end fetch unique landlordId from DB
#fetch exist landlordId from DB
query = {}
query['landlordInfo']={
    'landlordId' : 'group by',
}
existCols, existRows = crab.database.db(query,'select')
#end fetch exist landlordId from Db

landlordIds = [i[cols.index('landlordId')] for i in rows]
existLandlordIds = [i[existCols.index('landlordId')] for i in existRows]
newLandlordIds = [i for i in landlordIds if not i in existLandlordIds]

print 'searching %d new landlordIds for landlordInfo'%len(newLandlordIds)

for landlordId in np.random.permutation(newLandlordIds):
    try:
        format = crab.formator.formator('"content":{.+}\)')
        rawData = crab.locator.locator(urlProvidor(landlordId),format)

        if len(rawData) == 1:
            rawData = rawData[0]
            content = rawData[10:-2]
            content = eval(content)
        else:
            print 'passed landlordId : %d'%landlordId
            continue
        keys = ['landlordId','landlordName','landlordPersonRole','zhimaScore','mobileChecked','emailChecked',
                'realIdentity','realHeadImage','onlineReplyRate','avgConfirmMinutes','confirmRate','onlineRooms',
                'bookTotalCount','sex','ageGroup','zodiac','bloodType','education','profession','cityName',
                'hometown']
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
        json['landlordId'] = landlordId
        json['searchTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            json['avgConfirmMinutes'] = content['avgConfrimMinutes']
        except:
            pass
        change = {
            'landlordInfo' : json,
        }
        crab.database.db(change,'insert')
    except KeyboardInterrupt:
        exit()
    except:
        try:
            errorHandler = {}
            errorHandler['url'] = urlProvidor(landlordId)
            errorHandler['description'] = 'failed insert landlordInfo data of luId : %d'%landlordId
            errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            crab.database.db({'errorHandler':errorHandler},'insert')
        except:
            print 'passed landlordId %d with no DB errorHandler record'%landlordId
# except Exception as inst:
#     errorHandler = {}
#     errorHandler['url'] = urlProvidor(city,minprice,minprice+dprice)
#     errorHandler['description'] = inst.message
#     errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print 'error result in price : %d - %d '%(minprice,minprice+dprice)





if __name__ == 'main':
    pass


