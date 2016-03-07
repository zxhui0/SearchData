import crab
import time
import datetime
import ast
import numpy as np

City = ['Beijing','Shanghai','Xiamen','Guangzhou','Chengdu','Shenzhen','Xian','Nanjing','Hangzhou',
        'Chongqing','Wuhan','Suzhou','Wuxi','Qingdao','Sanya','Dalian','Haerbin','Kunming','Xianggang',
        'Shenyang','Zhengzhou']
CityId = [12,13,76,16,45,17,176,65,26,15,194,67,66,114,144,56,93,225,344,55,103]

assert len(City) == len(CityId)

def urlProvidor(cityid,minprice,maxprice):
    timestamp =  time.mktime(time.localtime())*1000
    url = 'http://wireless.xiaozhu.com/app/xzfk/html5/201/search/result?' \
          'jsonp=api_search_result&cityId={}&offset=0&length=10000&orderBy=recommend' \
          '&checkInDay=&checkOutDay=&leaseType=&minPrice={}&maxPrice={}&distId=&locId=' \
          '&keyword=&huXing=&facilitys=&guestNum=&cashPledgeFree=0&userId=0&sessId=0' \
          '&jsonp=api_search_result&timestamp={}&_={}'.format(
        cityid,minprice,maxprice,timestamp,timestamp+200
    )
    return url


# for string issues
true = True
false = False
#end string issues
format = crab.formator.formator('"item":\[.+\]')

for city in np.random.permutation(CityId):

    print 'fetching:'+City[CityId.index(city)]
    dprice = 3
    for minprice in range(1,1000,dprice+1):
        try:
            rawData = crab.locator.locator(urlProvidor(city,minprice,minprice+dprice),format)

            print 'searching price : %d - %d '%(minprice,minprice+dprice)

            if len(rawData) == 1:
                rawData = rawData[0]
                content = rawData[7:]
                content = eval(content)
            else:
                print 'empty result in price : %d - %d '%(minprice,minprice+dprice)
                continue


            for json in content:
                luId = {}
                luId['luId'] = json['luId']
                luId['cityId'] = city
                change ={'luId':luId}
                crab.database.db(change,'insert')
        except Exception as inst:
            errorHandler = {}
            errorHandler['url'] = urlProvidor(city,minprice,minprice+dprice)
            errorHandler['description'] = inst.message
            errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print 'error result in price : %d - %d '%(minprice,minprice+dprice)





if __name__ == 'main':
    pass

