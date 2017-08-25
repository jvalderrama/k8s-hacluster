#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By https://github.com/Tedezed

import sys, time, atexit, os
from signal import SIGTERM

class Daemon:
	""" A simple Daemon. Give it a pidfile location,
	it will write its pid to that and daemonize itself
	"""

	def __init__(self, pidfile, 
			stdin = '/dev/null', 
			stdout = '/dev/null', 
			stderr = '/dev/null'):
		self.pidfile = pidfile
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		

	def daemonize(self):
		""" Using the famous double-fork way 
		to daemonize!
		"""
		try:
			pid = os.fork()
			#exit from parent
			if pid > 0:
				sys.exit(0)

		except OSError, e:
			sys.stderr.write("Unable to do fork #1, %d-%s" %
					(e.errno, e.strerror))
			sys.exit(1)

		#independent identity from parent
		os.chdir("/")
		os.setsid()
		os.umask(0)


		try:
			pid = os.fork()

			#exit from parent
			if pid > 0:
				sys.exit(0)

		
		except OSError, e:
			sys.stderr.write("Unable to do fork #2, %d-%s" %
					(e.errno, e.strerror))
			sys.exit(1)

		#reset filestreams
		sys.stdout.flush()
		sys.stderr.flush() 	

		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)	

		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())

		atexit.register(self.onexit)
	
		#register the pid into the pidfile
		#this helps us to know whether daemon is 
		#running

		pf = file(self.pidfile, 'w+')
		pf.write('%s\n'% str(os.getpid()))
		pf.close()


	def onexit(self):
		#think of it as a SIGTERM handler
		os.remove(self.pidfile)	


	def run(self):
		return


	def start(self):
		try:
			pf = file(self.pidfile, 'r')	
			pid = int(pf.read().strip())
			pf.close()

		except IOError:
			pid = None

		if pid:
			sys.stderr.write("Daemon already running\n")
			sys.exit(1)

		self.daemonize()
		self.run()			


	def stop(self):
		try:
			pf = file(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()

		except IOError:
			pid = None

		if not pid:
			sys.stderr.write("Pidfile doesn't exist! "
					"Daemon not running?\n")
			#not an error for a restart.. so don't exit
			return
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)

		except OSError, e:
			err = str(e)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					#remove the pidfile
					os.remove(self.pidfile)			
					
			else:
				print str
				sys.exit(1)

	
	def restart(self):
		self.stop()
		self.start()
