#!/usr/bin/python 
import os
from shutil import copyfile


altran_ssh_key = "put-your-id-rsa-pub-key-here"

def create_ssh_key():
	if altran_ssh_key not in open('/home/vagrant/.ssh/authorized_keys').read():
		with open("/home/vagrant/.ssh/authorized_keys", "a") as auth_file:
			auth_file.write(altran_ssh_key)

def create_root_ssh_key_and_let_root_access():
	try:
		os.mkdir("/root/.ssh", 0755)
	except:
		print "File exists"
	copyfile("/home/vagrant/.ssh/authorized_keys","/root/.ssh/authorized_keys")

create_ssh_key()
create_root_ssh_key_and_let_root_access()
