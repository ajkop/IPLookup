#!/usr/env/python

import sys

try:
    from geolite2 import geolite2
except ImportError:
    raise ImportError('geolite2  is not installed (Run "pip install maxminddb-geolite2" first)')

ip_list = [ '70.124.166.33' , '91.201.116.241' , '95.213.177.124' , '185.234.217.11' , '87.98.146.134' , '46.17.41.64',
            '23.239.66.114' , '162.216.152.57' , '96.84.126.5' , '93.183.78.192']

def gen_dict(ip):
    reader = geolite2.reader()
    output = reader.get(ip)
    return output


def check_keys(iterable, keys):
    if isinstance(iterable, (list, tuple)):
        iterable = iterable[0]
    if keys[0] in iterable and len(keys) > 1:
        return check_keys(iterable[keys[0]], keys[1:])
    elif keys[0] in iterable:
        return iterable[keys[0]]
    else:
        return "Key: {} , was not found".format(keys[0].upper())


def iter_keys(ip):
    output = gen_dict(ip)
    if output:
        pass
    else:
        return "No lookup results"
    item_list = ({ "continent" : ["continent", "names", "en"] , "country" : ["country", "names", "en"] , "state" : ["subdivisions" , "names", "en"] ,
                    "city" : ["city" , "names" , "en"] , "accuracy_radius" : ["location", "accuracy_radius"] ,"latitude" : ["location", "latitude"] ,
                    "longitude" : ["location", "longitude"] , "time_zone" : ["location", "time_zone"] , "post_code" : ["postal", "code"]})
    return_dict = {}
    initial_return_list = {}
    for key, value in item_list.items():
        val = check_keys(output, value)
        initial_return_list.update({key.upper() : val})
    return_dict.update({ ip : initial_return_list})
    return return_dict

if __name__ == "__main__":
    for i in ip_list:
        result = iter_keys(i)
        print (result)
