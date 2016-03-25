import sqlite3,re,logging,time
import connector
logger = logging.getLogger('DB')
logger.setLevel(logging.WARNING)
fh = logging.FileHandler('database.log')
ch = logging.StreamHandler()
fh.setLevel(logging.DEBUG)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
logger.handlers
# conn = sqlite3.connect('crab.db') # local sqlite DB for dev

dbconfig={
"host":connector.HOST,
"user":connector.USER,
"password":connector.PASSWORD,
"database":connector.DB_NAME,
}
cnp = connector.connector.pooling.MySQLConnectionPool(
                    pool_name=None,
                    pool_size=20,
                    pool_reset_session=True,
                    **dbconfig)

# conn = connector.connector.connect(
#     host = connector.HOST,
#     user = connector.USER,
#     password = connector.PASSWORD,
#     database = connector.DB_NAME
# )

def db(change,method):
    conn = cnp.get_connection()
    c = conn.cursor()

    if(isinstance(method,basestring) & isinstance(change,dict)):
        logging.info('Correct input data kind for function db, using method %s'%method)
        if 'insert' == method.lower():
            for table,col_dict in change.iteritems():
                if(isinstance(col_dict,dict)):

                    size = len(col_dict)
                    if connector.BACKEND == 'sqlite':
                        colsNames = [_preprocessString(i) for i in col_dict.keys()]
                        colsValue = [_preprocessString(i) for i in col_dict.values()]
                        sqlquery = method.upper() + " INTO %s (%s) VALUES (%s)"%_sqlsafe(
                            (table,','.join(colsNames),','.join(colsValue))
                        )
                    elif connector.BACKEND == 'mysql':
                        colsNames = [i for i in col_dict.keys()]
                        colsValue = [_preprocessString(i) for i in col_dict.values()]
                        sqlquery = method.upper() + " INTO %s (%s) VALUES (%s)"%_sqlsafe(
                            (table,','.join(colsNames),','.join(colsValue))
                        )
                        time.sleep(0.001)
                    else:
                        colsNames = [_preprocessString(i) for i in col_dict.keys()]
                        colsValue = [_preprocessString(i) for i in col_dict.values()]
                        sqlquery = method.upper() + " INTO %s (%s) VALUES (%s)"%_sqlsafe(
                            (table,','.join(colsNames),','.join(colsValue))
                        )
                    try:
                        c.execute(sqlquery)
                        conn.commit()
                        time.sleep(0.001)
                        logger.info('Successful query : %s'%sqlquery)
                    except:
                        logger.error('Failed query : %s '%(sqlquery))
                else:
                    logger.error('Incorrect input data kind for function db, using method %s'%(method))
                    raise ValueError

            pass
        elif 'update' in method.lower():
            pass
        elif 'select' in method.lower():
            if(len(change) == 1):
                for table,col_dict in change.iteritems():
                    if(isinstance(col_dict,dict)):
                        if connector.BACKEND == 'sqlite':
                            logger.error('Please define sqlquery in sqlite')
                            raise ValueError
                        elif connector.BACKEND == 'mysql':

                            keys = [i for i in col_dict.keys() if isinstance(i,basestring)]
                            sqlquery = method.lower() + " %s FROM %s"%(','.join(keys),table)
                            where = []
                            for i,value in col_dict.iteritems():
                                if isinstance(value,basestring) & isinstance(i,basestring):
                                    if 'where' in value.lower():
                                        where.append(value.lower().replace('where',''))
                            if(where):
                                sqlquery = sqlquery + ' where %s'%_sqlsafe(' and '.join(where))
                            for i,value in col_dict.iteritems():
                                if isinstance(value,basestring) & isinstance(i,basestring):
                                    if 'group by' in value.lower():
                                        sqlquery = sqlquery + " group by %s"%_sqlsafe(i)
                                        break
                            try:
                                print sqlquery
                                c.execute(sqlquery)
                                logger.info('Successful query : %s'%sqlquery)
                                return keys,[i for i in c]
                            except:
                                logger.error('Failed query : %s '%(sqlquery))
                        else:
                            logger.error('Please define sqlquery in %s'%connector.BACKEND)
                            raise ValueError
                    else:
                        logger.error('Incorrect input data kind for function db, using method %s'%(method))
            else:
                logger.error('More than one table is defined in method %s'%method)
                raise ValueError
        else:
            raise ValueError
    else:
        logger.error('Incorrect input data kind for function db, using method %s'%method)
        raise ValueError
    conn.close()



def _sqlsafe(text_tuple):
    dangerous = ['insert','delete','drop','update','create','select']
    for text in text_tuple:
        if(isinstance(text,basestring)):
            for dan in dangerous:
                if dan in text.lower():
                    raise SQLSaftyError
    return text_tuple

class SQLSaftyError(BaseException):
    pass

def _preprocessString(x):
    if(isinstance(x,str)):
        if(connector.BACKEND == 'sqlite'):
            return "'%s'"%x
        elif(connector.BACKEND == 'mysql'):
            return "'%s'"%x
    elif(isinstance(x,list)):
        logger.error('_preprocessString illegal input')
        raise TypeError
    else:
        return "%s"%x
