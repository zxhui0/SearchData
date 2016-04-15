import crab
import time,Queue,threading
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
    endDate= (datetime.datetime.now()+datetime.timedelta(60,0)).strftime("%Y-%m-%d")


    url = 'http://wireless.xiaozhu.com/app/xzfk/html5/201/detail/Cal?jsonp=' \
        'detail_cal_callback&luId=%d&startDate=%s&endDate=%s&' \
        'userId=0&sessId=0&jsonp=detail_cal_callback'%(
        luId,today,endDate
        )
    return url



queueLock = threading.Lock()
class getluIdThreading(threading.Thread):
    def __init__(self,threadId,threadName,q):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.threadName = threadName
        self.q = q
    def run(self):
        # while not exitFlag:
        while True:
            queueLock.acquire()
            if not self.q.empty():
                luId = self.q.get()
                time.sleep(0+np.random.rand())
                queueLock.release()
                print 'thread:{} fetching luId:{}'.format(
                self.threadName,luId
                )
                time.sleep(0.1)
                getRawData(luId)
                compare(luId)
            else:
                queueLock.release()
                return None
        # else:
        #     print 'thread:{} finished'.format(
        #     self.threadName
        #     )
        #     time.sleep(0.1)
        #     queueLock.release()
        #     time.sleep(0.1)

def getRawData(luId):
    formator = crab.formator.formator('"content":\[{.+\]}\)')
    rawData = crab.locator.locator(urlProvidor(luId),formator)
    if rawData:
        rawData = rawData[0]
        content = rawData[10:-2]
        content = eval(content)
    else:
        print 'passed luId: %d'%luId
        return
    json={
    'luId':luId,
    'SearchTime':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'RawData':content,
    }
    crab.database.db({'priceCalendarRaw':json},'insert')

def compare(luId):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.datetime.now()-datetime.timedelta(1,0)).strftime("%Y-%m-%d")
    query = lambda x:{'priceCalendarRaw':{
    'luId':'group by','rawData':'where "%s"=DATE(SearchTime) AND luId=%s'%(x,luId)
    },}
    col,rawToday = crab.database.db(query(today),'select')
    col,rawYesterday = crab.database.db(query(yesterday),'select')
    if rawYesterday and rawToday:
        rawNew = eval(rawToday[0][col.index('rawData')])
        rawOld = eval(rawYesterday[0][col.index('rawData')])
        for new in rawNew:
            for old in rawOld:
                if new['day']==old['day']:
                    if new.keys()==old.keys():
                        for key in new.keys():
                            if new[key]!=old[key]:
                                change = {
                                'luId':luId,
                                'eventDate':new['day'],
                                'eventType':key,
                                'valueBefore':old[key],
                                'valueAfter':new[key],
                                'rawBefore':old,
                                'rawAfter':new,
                                'SearchTime':datetime.datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                                ),
                                }
                                crab.database.db(
                                {'bookingEvent':change}
                                ,'insert')

def getLuId(luId):
    # try:
    formator = crab.formator.formator('"content":\[{.+\]}\)')
    rawData = crab.locator.locator(urlProvidor(luId),formator)
    if len(rawData) == 1:
        rawData = rawData[0]
        content = rawData[10:-2]
        content = eval(content)
    else:
        print 'passed luId : %d'%luId
        return

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

    # except KeyboardInterrupt:
    #     exit()
    # except:
    #     try:
    #         errorHandler = {}
    #         errorHandler['url'] = urlProvidor(landlordId)
    #         errorHandler['description'] = 'failed insert priceCalendar data of luId : %d'%luId
    #         errorHandler['errorTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         crab.database.db({'errorHandler':errorHandler},'insert')
    #     except:
    #         print 'passed luId %d with no DB errorHandler record'%luId


if __name__ == '__main__':

    # for string issues
    true = True
    false = False
    null = ''
    #end string issues

    #fetch unique landlordId from DB
    query = {}
    query['luId']={
        'luId' : 'group by',
    }
    cols, rows = crab.database.db(query,'select')
    #end fetch unique landlordId from DB

    luIds = [i[cols.index('luId')] for i in rows]
    print 'searching %d luIds for priceCalendar'%len(luIds)


    json={}
    json['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json['activity'] = 'searchCalendar'
    json['status'] = 'starting'
    try:
        crab.database.db({'activityRecord':json},'insert')
    except:
        pass



    # threading in order to get information for each luId
    exitFlag = 0
    luIdQueue = Queue.Queue(12000)

    threadList = ['No. %d'%i for i in range(1)]
    threads=[]


    queueLock.acquire()
    luIdQueue.put(1716586435)
    for luId in np.random.permutation(luIds)[:0]:
        luIdQueue.put(luId)

    for name in threadList:
        thread = getluIdThreading(
        threadList.index(name),
        name,
        luIdQueue)
        thread.start()
        threads.append(thread)

    queueLock.release()


    # while not luIdQueue.empty():
    #     pass
    #
    # exitFlag = 1
    # print 'Empty queue'

    for t in threads:
        t.join()

    print 'All Queue Finished'
    json={}
    json['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json['activity'] = 'searchCalendar'
    json['status'] = 'finished'
    try:
        crab.database.db({'activityRecord':json},'insert')
    except:
        pass
