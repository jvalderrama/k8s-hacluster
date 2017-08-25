External Loadbalancer for Kubernetes
====================================

Inspired by [service-loadbalancer](https://github.com/kubernetes/contrib/tree/master/service-loadbalancer)

#### Instalation

Install basic sowftware

	yum install epel-release
	yum install haproxy git socat python-pip
	pip install jinja2
	pip install deepdiff

Clone repository in /

	git clone https://github.com/Tedezed/Celtic-Kubernetes.git

Create errors html

	mkdir /etc/haproxy/errors/
	cp /Celtic-Kubernetes/external_loadbalancer_hap/errors/* /etc/haproxy/errors/
	cp /Celtic-Kubernetes/external_loadbalancer_hap/system/haproxy.cfg /etc/haproxy/

Create state global

	mkdir -p /var/state/haproxy/
	touch  /var/state/haproxy/global

Modify configuration.json
	
	{
	"kube_api": "morrigan:8080",
	"version": "v1",
	"file_conf": "template.cfg",
	"stats": true,
	"sleep": 3
	}

* Kube API master
	
		"kube_api": "10.0.0.39:8080"

Enable Haproxy

	systemctl enable haproxy

#### Test

	python hap_manager_daemon.py start
	python hap_manager_daemon.py stop
	sh haproxy_reload
	
#### Unit for systemd

Copy file hap_manager.service

	cp /Celtic-Kubernetes/external_loadbalancer_hap/system/hap_manager.service /lib/systemd/system/hap_manager.service

Modify permissions

	chmod 644 /lib/systemd/system/hap_manager.service

Reload daemon systemctl

	systemctl daemon-reload

Start hap_manager.service

	systemctl start hap_manager.service

	systemctl enable hap_manager.service

See settings

	cat /etc/haproxy/haproxy.cfg | grep acl

#### Define services

Example rc

	apiVersion: v1
	kind: ReplicationController
	metadata:
	 name: nginx-controller
	spec:
	 replicas: 2
	 selector:
	   name: nginx
	 template:
	   metadata:
	     labels:
	       name: nginx
	   spec:
	     containers:
	       - name: nginx
	         image: nginx
	         ports:
	           - containerPort: 80

Example svc

	apiVersion: v1
	kind: Service
	metadata:
	  name: nginx-service-domain
	  labels:
	    app: nginx
	spec:
	  type: NodePort
	  ports:
	  - port: 80
	    protocol: TCP
	    name: http
	  selector:
	    name: nginx

Enter with `http://IP-SERVER-HAP/NAME-SERVICE/`

You need domain for the service, no problem

Example svc with domain

	apiVersion: v1
	kind: Service
	metadata:
	  name: nginx-service-domain
	  labels:
	    app: nginx
	    domain: www.test-domain.com
	spec:
	  type: NodePort
	  ports:
	  - port: 80
	    protocol: TCP
	    name: http
	  selector:
	    name: nginx
