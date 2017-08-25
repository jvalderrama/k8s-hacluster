#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By https://github.com/Tedezed

import sys
from daemon import Daemon
import os
import requests

from json import loads, load
from requests import get
from time import sleep, strftime
from deepdiff import DeepDiff
from manager_tools import *
from write_template import *

class MyDaemon(Daemon):
	def run(self):
		while True:
			self.hap_manager()

	def hap_manager(self):
		try:
			data = get_conf(directory,'configuration.json')
			kube_api = data["kube_api"]
			version = data["version"]
			time_sleep = data["sleep"]

			dic_svc_old = {}
			while True:
				dic_svc_actives = {}
				get_json_svcs = get_kube_api(kube_api, version, 'services')['items']
				for svc in get_json_svcs:
					try:
						svc_node_port = svc['spec']['ports'][0]['nodePort']
						svc_name = svc['metadata']['name']
						if svc_name not in dic_svc_actives:
							dic_svc_actives[svc_name] = svc_node_port
					except KeyError:
						pass
				ddiff = DeepDiff(dic_svc_actives, dic_svc_old)
			 	if ddiff:
				 	print "Reload HAProxy"
				 	write_template_conf(directory)
				 	reload_hap()
				dic_svc_old = dic_svc_actives
				sleep(time_sleep)
		except IOError as e:
			sys.stderr.write("[ %s ] I/O error(%s)\n" % (strftime("%H:%M:%S"), e))
			sleep(10)
		except NameError as e:
			sys.stderr.write("[ %s ] NameError (%s)\n" % (strftime("%H:%M:%S"), e))
			sleep(10)
		sleep(2)


if __name__ == "__main__":
	daemon = MyDaemon("/var/run/hap_manager.pid")
	global directory 
	directory = os.path.dirname(os.path.realpath(__file__))+"/"
	if (len(sys.argv) == 2):
		if sys.argv[1] == 'start':
			daemon.start()

		elif sys.argv[1] == 'stop':
			daemon.stop()

		elif sys.argv[1] == 'restart':
			daemon.restart()

		else:
			print "Unknown command!"
			sys.exit(2)
		
		sys.exit(0)	

	else:
		print "Usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
