#!/usr/bin/env python
#coding:utf-8

import hashlib
import time
import random
import platform


def generate_trace_id():
  hostname = platform.node()
  return hashlib.md5((str(time.time() * 100) + getHostName() + str(random.randint(1, 1000000))).encode()).hexdigest()[8:16]

def getHostName():
  return platform.node()
