import re,logging,sqlite3
# logging.basicConfig(filename='formator.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)
logger = logging.getLogger('formater')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('formater.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# conn = sqlite3.connect('crab.db')
# c = conn.cursor()
# c.execute("SELECT name FROM sqlite_master  where type='table'")
# SearchSpaceSet = [i[0] for i in c.fetchall()]

class formator(object):
    def __init__(self,RELocator):
        if(isinstance(RELocator,basestring)):
            try:
                self.RELocator = [re.compile(RELocator)]
            except:
                logger.error('Illegal RELocator: %s'%RELocator)
                raise ValueError
        elif isinstance(RELocator,list):
            try:
                self.RELocator = [re.compile(i) for i in RELocator]
            except:
                logger.error('Illegal RELocator list')
                raise ValueError
        else:
            logger.error('Illegal RELocator kind')
            raise ValueError




