#!/bin/bash
ssh-keygen -f "/home/altran/.ssh/known_hosts" -R 10.10.10.60
ssh-copy-id -o StrictHostKeyChecking=no root@10.10.10.60
ssh-keygen -f "/home/altran/.ssh/known_hosts" -R 10.10.10.61
ssh-copy-id -o StrictHostKeyChecking=no root@10.10.10.61
ssh-keygen -f "/home/altran/.ssh/known_hosts" -R 10.10.10.62
ssh-copy-id -o StrictHostKeyChecking=no root@10.10.10.62
ssh-keygen -f "/home/altran/.ssh/known_hosts" -R 10.10.10.63
ssh-copy-id -o StrictHostKeyChecking=no root@10.10.10.63
ssh-keygen -f "/home/altran/.ssh/known_hosts" -R 10.10.10.64
ssh-copy-id -o StrictHostKeyChecking=no root@10.10.10.64
#ssh-keygen -f "/home/altran/.ssh/known_hosts" -R 10.10.10.65
#ssh-copy-id -o StrictHostKeyChecking=no root@10.10.10.65
#ssh-keygen -f "/home/altran/.ssh/known_hosts" -R 10.10.10.66
#ssh-copy-id -o StrictHostKeyChecking=no root@10.10.10.66
ssh-keygen -f "/home/altran/.ssh/known_hosts" -R 10.10.10.67
ssh-copy-id -o StrictHostKeyChecking=no root@10.10.10.67
