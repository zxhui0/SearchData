import sys, inspect, logging,re
import formator,database,generator,locator
# logging.basicConfig(filename='tests.log',format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.DEBUG)

# class isformatworking(object):
#     a = formator.formator(SearchSpace='room',RELocator='^pi')
#     a = formator.formator(RELocator='^house',SearchSpace='room',REexclusion=['^ye','\w'])
#     a=formator.formator(RELocator='^house',SearchSpace='host',REexclusion=['^ye','\w'])
#
#     try:
#         a=formator.formator(RELocator='^house',SearchSpace='people',REexclusion=['^ye','\w'])
#     except ValueError:
#         pass
#     else:
#         raise AssertionError
#
#     try:
#         a=formator.formator(RELocator='^house',SearchSpace='',REexclusion=['^ye','\w'])
#     except ValueError:
#         pass
#     else:
#         raise AssertionError
#
#     try:
#         a=formator.formator(RELocator='^house',SearchSpace='',REexclusion=[''])
#     except ValueError:
#         pass
#     else:
#         raise AssertionError
#
# class iserrorHandlerworking(object):
#     urlItem = generator.urlItem(url = 'https://docs.python.org/2/howto/urllib2.html',type='room')
#     format = formator.formator(RELocator=[
#         '<div class="section" id="\w+">\n<h2>\w+<a class="headerlink"',
#         '>\w+<',
#         '\w+'
#     ],SearchSpace='room',REexclusion=['^ye','\w'])
#     locator.locator(urlItem,format)

class isDBworking(object):
    json = {
        'page':{
            'num':'405'
        }
    }
    database.db(json,'insert')
    json = {
        'page':{
            'num':'group by'
        }
    }
    header,value = database.db(json,'select')








