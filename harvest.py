from cache import Cache
from urllib2 import urlopen
from json import load
from argparse import ArgumentParser
from datetime import datetime
from time import mktime

from key import WUNDER_KEY

BASE_URL = "http://api.wunderground.com/api/"+WUNDER_KEY+"/%s/q/MI/%s.json"

def add_current(cache, response=None, base_url=None, zipcode=None):
    if response==None:
        resp = load(urlopen(base_url % ('conditions', zipcode)))
    else:
        resp = response
    date = resp['current_observation']['observation_epoch']
    temp = resp['current_observation']['temp_f']
    
    cache.put(str(zipcode)+'_'+str(date), temp)
    
def add_historical(cache, response=None, base_url=None, request_date=None, zipcode=None):
    if response==None:
        resp = load(urlopen(base_url % ('history_'+request_date, zipcode)))
    else:
        resp = response
    for observation in resp['history']['observations']:
        date = observation['date']
        date = datetime(int(date['year']), int(date['mon']), int(date['mday']), int(date['hour']), int(date['min']), 0)
        date = mktime(date.timetuple())
        temp = observation['tempi']
        
        cache.put(str(zipcode)+'_'+str(date), temp)
    
    
if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('-c', '--current', help="Add Current temp to cache", action="store_true")
    options.add_argument('-z', '--zip-code', default="48654")
    options.add_argument('-i', '--historical', help="Add the temps for some historical date.", action="store_true")
    options.add_argument('-d', '--date', help="For historical requests, what date?  Should be YYYYMMDD", default = datetime.now().strftime('%Y%m%d'))
    options = options.parse_args()
    
    print "Using options: " + str(options)
    
    cache = Cache("temps.db", reset=False)
    
    if options.current and options.historical:
        resp = load(urlopen(BASE_URL % ('conditions/history_' + options.date, options.zip_code)))
        add_current(cache, response = resp, zipcode=options.zip_code)
        add_historical(cache, response = resp, zipcode=options.zip_code)
    elif options.current:
        add_current(cache, base_url=BASE_URL, zipcode=options.zip_code)
    elif options.historical:
        add_historical(cache, base_url=BASE_URL, request_date=options.date, zipcode=options.zip_code)
    
    
    