#!/usr/bin/env python
#coding:utf-8

import mlog4py
logger = mlog4py.getLogger(__name__)

def mult(a,b):
  logger.debug('mult: %d, %d' %(a,b))
  return a*b
