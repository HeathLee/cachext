from .peewee import *

TESTING = False
DEBUG = True

MIDDLEWARES = [
    'sea.middleware.ServiceLogMiddleware',
    'sea.middleware.RpcErrorMiddleware',
    'cachext.sea.cachextMiddleware'
]
