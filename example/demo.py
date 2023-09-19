#!/usr/bin/env python
#coding:utf-8

import mlog4py
# 优先加载
mlog4py.basicConfig(app='appname',level=mlog4py.DEBUG,filename="mlog.log")


# 加载其它项目库
import os
import time
import libs

logger = mlog4py.getLogger(__name__)



if __name__ == '__main__':

  # 配置日志变量
  logger.setExtra(tags='app_start')
  # INFO
  logger.info('App进程start.')
  # DEBUG
  logger.debug('This is a debug log.')
  # WARNING
  logger.warning('This is a warning log.')
  # ERROR
  logger.error('This is a error log.')
  # CRITICAL
  logger.critical('This is a critical log.')
  # call function
  logger.debug('libs mult call: %d ' %(libs.mult(2,3)), tags="call_nult")
  #end
  logger.info('App进程end', tags="app_end")
