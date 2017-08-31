# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'json'
require 'fileutils'

flag = 0

Vagrant.configure(2) do |config|
    servers = JSON.parse(File.read(File.join(File.dirname(__FILE__), 'infraestructure.json')))
        servers.each do |server|
	    config.ssh.forward_x11 = true
            config.vm.define server['name'] do |srv|
      	        srv.vm.box_url = server['box_url']
		srv.vm.box = server['box']
	        srv.ssh.insert_key = server['insert_key']
	        srv.vm.hostname = server['name']
  	        srv.vm.network 'private_network', :ip => server['ip_addr']
        	srv.vm.synced_folder ".", "/home/vagrant/sync", disabled: server['disable_synched_folder']
                srv.vm.provider :libvirt do |v|
		    # Quitamos el prefix para que no nos ponga por defecto 
		    # la carpeta en nombre
		    v.default_prefix = ""
		    # Cargamos URI y drivers por CA certificate problem
	            v.uri = 'qemu+unix:///system'
		    v.driver = 'kvm'
		    v.host = server['name']
		    v.memory = server['ram']
		    v.cpus = server['cpu']
      		end
 
 	    config.vm.provision "shell", path: "./scripts/get_pip.py"		
	    config.vm.provision "shell", path: "./scripts/prepare_cluster.py"

		srv.vm.provision "shell", inline: <<-SHELL
		    set -e
		    systemctl restart network
	            echo "root:root" | chpasswd
		SHELL

        flag += 1
        if flag == servers.length
                srv.vm.provision :ansible do |ansible|
                 ansible.playbook = "ansible/kubernetes.yml"
                 ansible.inventory_path = "ansible/hosts"
                 ansible.limit = "all"
               end
        end

        end
    end
end
