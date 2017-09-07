# High Availability Kubernetes Cluster + Scaling 

Deploy kubernetes on the fly, the project creates a **HA kubernetes cluster** ``two master nodes, two minions 
nodes and two poxies nodes``, it uses **Vagrant** with **KVM** as infrastecture provider (IaaS) and 
**Ansible** as configuration manager to automatically have a ready and functional **HA kubernetes cluster** 
in less than 15 minutes. 

Finally it deploys two **kubernetes nginx services** these two test the balance between proxies for different 
requests and an **api** to make a request to the proxies from a browser.

As an extra the entire **HA kubernetes cluster** can be scalable if wished, the project has a **k8s-scale** project
to **add a new minion** to the existing cluster.  

Reference: http://tedezed.github.io/Celtic-Kubernetes/HTML/3-Kube_HA_pcs.html

![alt text](http://tedezed.github.io/Celtic-Kubernetes/HTML/Imagenes/topo2.jpg)

## 1. Pre-requisites

* Localhost machine with Linux distribution
* KVM
* Vagrant 1.8.1 or higher
* Vagrant libvirt plugin for KVM
* Ansible 2.2.1 or higher

## 2. Prepare your localhost environment

The first thing is check that you localhost support virtualization, just type 
``egrep -c '(vmx|svm)' /proc/cpuinfo`` if the result is ``0``, your localhost does not support it, 
in other case ``> 0``, means you locahost support virtualization, but also must be ensured it is enable 
in the BIOS. Once it is assured procced to install ``kvm`` (https://www.linux-kvm.org/page/Downloads).

Next to complete the environment and reproduce the ``kubernetes cluster``, 
with the use of ``Vagrant`` just install it (https://www.vagrantup.com/) on your localhost and must be 
installed ``Ansible`` also (http://docs.ansible.com/ansible/latest/intro_installation.html).

In the other hand to use ``kvm`` to setup kubernetes cluster nodes, must be installed the ``vagrant libvirt provider``,
it is a ``plugin`` for ``vagrant`` to use with ``libvirt`` API to manage ``kvm`` as infraestructure provider.
(https://github.com/vagrant-libvirt/vagrant-libvirt#installation) 

Finally we need a ``Public RSA Key`` to inject in the ``Kubernetes Cluster`` nodes, therefore if you have already 
one fine, it is going to be used later, otherwise proceed to ``Generate SSH Keys`` in your localhost
(https://www.cyberciti.biz/faq/linux-unix-generating-ssh-keys/)

## 3. Setup your kubernetes cluster

* In the localhost just clone the repository   
   ``git clone https://github.com/jvalderrama/k8s-hacluster.git``

* Go inside the folder k8s-hacluster  
   ``cd k8s-hacluster``

* Set your ``Publis RSA Key`` in the script ``scripts/prepare_cluster.py``, generally it is located in ~/.ssh/id_rsa.pub

* Start up the ``Kubernetes Cluster``  
   ``vagrant up --provider libvirt``

That's all ...

## 4. Check your Kubernetes Cluster

Now check the entire cluster with the next tips

* Go to minion-1 node and check nodes  
  ``vagrant ssh Alcazaba-minion-1``  
  ``kubectl -s http://10.10.10.69:8080 get nodes`` it must show the two minions nodes ready and working

* Go to minion-2 node and check nodes  
  ``vagrant ssh Caballo-minion-2``  
  ``kubectl config set-cluster test-cluster --server=http://10.10.10.69:8080``  
  ``kubectl config set-context test-cluster --cluster=test-cluster``  
  ``kubectl config use-context test-cluster``  
  ``kubectl get nodes`` it must show the two minions nodes ready and working

* Go to master node and check nodes  
  ``vagrant ssh Mulhacen-master-1``  
  ``kubectl cluster-info``  

  ``sudo pcs cluster status``  
  ``sudo pcs resource show``  

* Go to proxy-1 node and check nodes  
  ``vagrant ssh Caldera-proxy-1``  
  ``sudo pcs cluster status``  
  ``sudo pcs resource show``  

* Finally in localhost check the "Nginx services welcome page"  
  ``curl 10.10.10.68/nginx-service-domain/``  
  ``curl 10.10.10.68/nginx-service-domain-2/``
  
  From a browser  
  ``http://10.10.10.68:8080/avg/authservice/rest/imsi``

## 5. Scale the existing HA Kubernetes Cluster

Follow the next steps to scale up your entire cluster  

* Go inside the folder k8s-scale  
  ``cd k8s-hacluster/k8s-scale/``  
  
* Start up the new Minion node to add in the ``Kubernetes Cluster``  
   ``vagrant up --provider libvirt``  

* Go to master node and check minion nodes  
  ``vagrant ssh Mulhacen-master-1``  
  ``kubectl get nodes``  

* Go to master node and check minion nodes (Must be appears three nodes)  
  ``vagrant ssh Mulhacen-master-1``  
  ``kubectl get nodes``  

* Deploy a new pod inside the new minion node  
  ``Replace file in /tmp/avg-api-rc.yml in line 6 **replicas: 2** key by **replicas: 3**``   
  ``kubectl replace rc --filename=/tmp/avg-api-rc.yml``   

* Check the new pod deployed in the new minion node (Must be appears three avg-api-controller-*, one of these deployed
  in the new minion node)  
  ``kubectl get pods``  

That's all, cluster has been scaled up !!!

## 5. Credits

Thanks also to my partners @Noel_illo (Noel Ruiz Lopez) and @M4nu_sL (Manuel Sanchez Lopez) for your great job :)
