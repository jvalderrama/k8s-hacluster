#!/usr/bin/python 
import os
from shutil import copyfile


altran_ssh_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDJRlWP53248RcczMqCX5nom+YsoMKWX8LFQVVGGi/SRiBRr8fo2L6ESOg71zEnJYgB456DRk9V++n8fApHV9TV/NyfjGmq+6Nuqbgva7QVd/EEv4skAt4rh7JEBKTOcDqQX2+LP8OQ8/YAfWENAV/SOjTnpdi6GI17TS3uakZTJKvBHXXqI5cRLPETjyvqLcTp4dyxbL3Mgd+D4/pd9FzpI33HxnEX/QlQYcHLeqqEH5IL0GP/4Htuq37WT2GdgD35X86yGeomeE0MIoUXEm0hIk7QiyJOhShF2kLlfgdyLGUpmKQPgIUZsoEuXNAEVh8J6iHHkhAcUVNWvqsEN63H altran@altran-Latitude-E5420"

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
