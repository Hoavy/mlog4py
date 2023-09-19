#!/usr/bin/env python
#coding:utf-8

import logging

try:
    import thread
    import threading
except ImportError:
    thread = None

try:
  from utils import generate_trace_id,getHostName
except ImportError:
  from mlog4py.utils import generate_trace_id,getHostName

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARN
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


class MLoggerAdapter(logging.LoggerAdapter):
  def process(self, msg, kwargs):
    kwarg = {}
    if 'extra' not in kwarg:
      kwarg["extra"] = self.extra

    if 'tags' in kwargs:
      kwarg["extra"]['tags'] =  kwargs['tags']

    if 'traceid' in kwargs:
      kwarg["extra"]['traceid'] =  kwargs['traceid']

    if 'spanid' in kwargs:
      kwarg["extra"]['spanid'] =  kwargs['spanid']

    return msg, kwarg

  def setExtra(self,**kwargs):
    if 'tags' in kwargs:
      self.extra['tags'] =  kwargs['tags']

    if 'traceid' in kwargs:
      self.extra['traceid'] =  kwargs['traceid']

    if 'spanid' in kwargs:
      self.extra['spanid'] =  kwargs['spanid']

  def initTraceid(self):
    self.extra['traceid'] = generate_trace_id()

class MLoger(object):
  def __init__(self, name, level=logging.DEBUG,filename=None):
    self.name = name
    self.filename = filename
    self.level = level
    self.appName = None
    self.traceID = None
    self.spanID = None
    self.tags = None
    self.config = None
    self.logger = None
    self.extra_dict = {"psm":'-',"traceid": '-', "spanid": '-', "hostname": '-', "tags": '-'}
    self.formatter = "%(levelname)s|%(psm)s|%(asctime)s.%(msecs)03d+08:00|%(traceid)s|%(spanid)s|%(hostname)s|%(tags)s|%(message)s"


  def setBasicConfig(self,*kwargs):
    self.config = kwargs

  def setLevel(self,level):
    self.level = level

  def setFileName(self,filename,path='/data/logs'):
      self.filename = r"%s/%s" %(path,filename)

  def setTraceID(self,id):
    self.traceID = id

  def setSpanID(self,id):
    self.spanID = id

  def setTags(self,tag):
    self.tags = tag

  def setAppName(self,app):
    self.appName = app

  def loadBasicConfig(self):
    logging.basicConfig(filename=self.filename, level=self.level, format=self.formatter, datefmt='%Y-%m-%dT%I:%M:%S')

  # 配置session变量
  def initSession(self):
    for key in self.extra_dict:
      if 'psm' is key:
        self.extra_dict[key] = self.appName
      if 'traceid' is key:
        self.extra_dict[key] = generate_trace_id()
      if 'hostname' is key:
        self.extra_dict[key] = getHostName()

  def getLogger(self,name):
    if self.logger is None:
      self.loadBasicConfig()
      self.initSession()
      logger = logging.getLogger(name)
      self.logger = MLoggerAdapter(logger, self.extra_dict)
    return self.logger

class RootLogger(MLoger):
  def __init__(self, level):
    MLoger.__init__(self, "root", level)

root = RootLogger(logging.DEBUG)

if thread:
    _lock = threading.RLock()
else:
    _lock = None

def _acquireLock():
    if _lock:
        _lock.acquire()

def _releaseLock():
    if _lock:
        _lock.release()


# 配置
def basicConfig(**kwargs):
  _acquireLock()
  try:
    filename = kwargs.get("filename")
    path = kwargs.get("filepath")
    if filename and path:
      root.setFileName(filename,path)
    else:
      root.setFileName(filename)

    level = kwargs.get("level")
    if level is not None:
      root.setLevel(level)

    app = kwargs.get("app")
    if app is not None:
      root.setAppName(app)

  finally:
      _releaseLock()

def getLogger(name=None):
  if not name or isinstance(name, str) and name == root.name:
      return root.logger
  return root.getLogger(name)
