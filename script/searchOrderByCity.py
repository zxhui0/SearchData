import crab
import time
import datetime
import ast

City = ['Beijing','Shanghai','Xiamen','Guangzhou','Chengdu','Shenzhen','Xian','Nanjing','Hangzhou',
        'Chongqing','Wuhan','Suzhou','Wuxi','Qingdao','Sanya','Dalian','Haerbin','Kunming','Xianggang',
        'Shenyang','Zhengzhou']
CityId = [12,13,76,16,45,17,176,65,26,15,194,67,66,114,144,56,93,225,344,55,103]

assert len(City) == len(CityId)

def urlProvidor(cityid):
    timestamp =  time.mktime(time.localtime())*1000
    url = 'http://wireless.xiaozhu.com/app/xzfk/html5/201/search/result?' \
          'jsonp=api_search_result&cityId={}&offset=0&length=10000&orderBy=recommend' \
          '&checkInDay=&checkOutDay=&leaseType=&minPrice=0&maxPrice=&distId=&locId=' \
          '&keyword=&huXing=&facilitys=&guestNum=&cashPledgeFree=0&userId=0&sessId=0' \
          '&jsonp=api_search_result&timestamp={}&_={}'.format(
        cityid,timestamp,timestamp+200
    )
    return url


# for string issues
true = True
false = False
#end string issues
format = crab.formator.formator('"item":\[.+\]')

json={}
json['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json['activity'] = 'searchOrder'
json['status'] = 'starting'
try:
    crab.database.db({'activityRecord':json},'insert')
except:
    pass

for name , city in enumerate(CityId):


    print 'fetching:'+City[name]

    try:

        rawData = crab.locator.locator(urlProvidor(city),format)


        if len(rawData) == 1:
            rawData = rawData[0]
            content = rawData[7:]
            content = eval(content)
        else:
            continue


        for order,json in enumerate(content):
            SearchOrder = {}
            SearchOrder['luId'] = json['luId']
            SearchOrder['listOrder'] = order
            SearchOrder['searchTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            SearchOrder['cityId'] = city
            change ={'SearchOrder':SearchOrder}
            crab.database.db(change,'insert')
    except:
        try:
            errorHandler = {}
            errorHandler['url'] = urlProvidor(city)
            errorHandler['description'] = 'failed insert searchOrder data of city: %s'%City[name]
            errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            crab.database.db({'errorHandler':errorHandler},'insert')
        except:
            pass

json={}
json['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json['activity'] = 'searchOrder'
json['status'] = 'ending'
try:
    crab.database.db({'activityRecord':json},'insert')
except:
    pass



if __name__ == 'main':
    pass
