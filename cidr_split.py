#!/usr/env/python
from ip_lookup import iter_keys
from netaddr import IPNetwork

ip_range = "19.185.205.94/24"

def split_cidr(ip_range):
    stripped_list = []
    cidr_dict = {}
    ip_range = ip_range.strip()
    ip_list = IPNetwork('{}'.format(ip_range))
    cidr_len = "Length : {}".format(ip_list.size)
    ip_obj = "Block : {}".format(str(ip_list))
    for ip in ip_list:
        ip = str(ip)
        ip = ip.strip()
        stripped_list.append(ip)
    cidr_dict.update({ "{} , {}".format(ip_obj, cidr_len) : stripped_list})
    return cidr_dict

if __name__ == "__main__":
    return_dict = split_cidr(ip_range)
    for key,value in return_dict.items():
        for ip in value:
            print (ip)
