#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By https://github.com/Tedezed

import sys
from os import system, path
from json import loads, load
from requests import get
from jinja2 import Environment, FileSystemLoader

def get_kube_api(kube_api, version, get_type):
	request = get('http://%s/api/%s/%s/' % (kube_api, version, get_type))
	json_api = loads(request.text)
	return json_api

# Load configuration
def get_conf(directory, json_conf):
	with open(directory+json_conf) as data_file:    
    		data = load(data_file)
    	return data

def reload_hap():
	#system('sudo sh haproxy_reload')
	system("service haproxy reload")

def constraint_domain(kube_api, version, new_domain):
	get_json = get_kube_api(kube_api, version, 'services')['items']

	key = False
	for service in get_json:
		try:
			domain_in_use = service['metadata']['labels']['domain']
			if new_domain == domain_in_use:
				key = True
		except KeyError:
			pass
	return key
