import sqlite3,logging,database

logger = logging.getLogger('generator')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('generator.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# conn = sqlite3.connect('crab.db')
# c = conn.cursor()
# c.execute(
#     "PRAGMA table_info(URL)"
# )
# fecthResult = c.fetchall()
# colName={i[1]:fecthResult.index(i) for i in fecthResult}
#
# def generator(select="lastVisit < datetime('now')"):
#     c.execute(
#         "select * from URL where %s"%database._sqlsafe(select)
#     )
#     logging.info('Successful query from URL using select = %s'%select)
#     for colValue in c.fetchall():
#         yield urlItem(
#             url = colValue[colName[u'url']],type=colValue[colName[u'type']]
#         )
#
# class urlItem(object):
#     def __init__(self,url,type):
#         self.url = url
#         self.type = type






