import crab
import time
import datetime
import ast
import numpy as np

City = ['Beijing','Shanghai','Xiamen','Guangzhou','Chengdu','Shenzhen','Xian','Nanjing','Hangzhou',
        'Chongqing','Wuhan','Suzhou','Wuxi','Qingdao','Sanya','Dalian','Haerbin','Kunming','Xianggang',
        'Shenyang','Zhengzhou']
CityId = [12,13,76,16,45,17,176,65,26,15,194,67,66,114,144,56,93,225,344,55,103]
City =['Beijing','Shanghai','Xiamen','Guangzhou','Sanya']
CityId = [12,13,76,16,144]
assert len(City) == len(CityId)

def urlProvidor(cityid):
    timestamp =  time.mktime(time.localtime())*1000
    dict = {
    'Shanghai':'http://sh.xiaozhu.com/sitemap.xml',
    'Beijing':'http://bj.xiaozhu.com/sitemap.xml',
    'Sanya':'http://sanya.xiaozhu.com/sitemap.xml',
    'Xiamen':'http://xm.xiaozhu.com/sitemap.xml',
    'Guangzhou':'http://gz.xiaozhu.com/sitemap.xml',
    }
    if cityid in CityId:
        cityname = City[CityId.index(cityid)]
    else:
        return None
    url = dict[cityname]
    return url


# for string issues
true = True
false = False
#end string issues


json={}
json['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json['activity'] = 'searchLuid'
json['status'] = 'starting'
try:
    crab.database.db({'activityRecord':json},'insert')
except:
    pass

#existing luIds
query = {}
query['luId']={
    'luId' : 'group by',
}
cols, rows = crab.database.db(query,'select')
#end fetch unique landlordId from DB

luIds = [i[cols.index('luId')] for i in rows]
# print '%d existing luIds'%len(luIds)
#end fetching

format = crab.formator.formator('/fangzi/[^<]+\.html</loc>')

for city in np.random.permutation(CityId):

    print 'fetching:'+City[CityId.index(city)]
    url = urlProvidor(city)
    if not url:
        break
    rawData = crab.locator.locator(url,format)
    for line in rawData:
        luId = {}
        luId['luId'] = line[len('/fangzi/'):-len('.html</loc>')]
        luId['cityId'] = city
        if int(luId['luId']) not in luIds:
            change ={'luId':luId}
            crab.database.db(change,'insert')
            # print 'updated %s'%luId['luId']
        #     for json in content:
        #         luId = {}
        #         luId['luId'] = json['luId']
        #         luId['cityId'] = city
        #         change ={'luId':luId}
        #         crab.database.db(change,'insert')
        # except Exception as inst:
        #     errorHandler = {}
        #     errorHandler['url'] = urlProvidor(city,minprice,minprice+dprice)
        #     errorHandler['description'] = inst.message
        #     errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     print 'error result in price : %d - %d '%(minprice,minprice+dprice)
        #
        #
        #

json={}
json['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
json['activity'] = 'searchLuid'
json['status'] = 'finished'
try:
    crab.database.db({'activityRecord':json},'insert')
except:
    pass

if __name__ == 'main':
    pass
