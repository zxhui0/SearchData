import re,formator,generator,urllib2,logging,database,datetime

logger = logging.getLogger('locator')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('locator.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def locator(url,formatItem):
    if(
            isinstance(url,basestring)
                &isinstance(formatItem,formator.formator)
    ):
        try:
            context = []
            UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'
            header = {'User-Agent':UserAgent}
            request = urllib2.Request(url,headers=header)
            response = urllib2.urlopen(request)
            context = response.read()
            for relocator in formatItem.RELocator:
                context = re.findall(relocator,context)
            return context
        except urllib2.URLError:
            logger.error('URLError happened on url: %s'%url)
            change={
                'errorHandler':{
                    'url':url,
                    'description':'URL reading Error',
                    'errorTime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            database.db(change=change,method="insert")

    else:
        logger.error('Illegal data type for locator')
        raise TypeError