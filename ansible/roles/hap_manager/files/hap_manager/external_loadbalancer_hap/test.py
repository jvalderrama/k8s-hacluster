#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By https://github.com/Tedezed

# Test1
#from write_template import *
#import os
#directory = os.path.dirname(os.path.realpath(__file__))+"/"
#write_template_conf(directory)

# Test2
from write_template import *
print constraint_domain('172.22.205.249:8080', 'v1', 'www.test-domain.com')