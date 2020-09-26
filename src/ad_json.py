#coding=utf-8

import abc
import json

class AdJson(object):
    _CONTAINER_NAME = "_container"
    def __init__(self, *args, **kwargs):
        self.__dict__[self._CONTAINER_NAME] = {}

        for arg in args:
            self._proc_dict_para(arg)

        for key, value in kwargs.items():
            self[key] = value

    def __getattr__(self, name):
        print("get attr", name)
        return self[name]

    def __setattr__(self, name, value):
        print("set attr", name)
        self[name] = value

    def __getitem__(self, key):
        print("get item", key)
        return self._container.get(key)

    def __setitem__(self, key, value):
        print("set item", key)
        
        if isinstance(value, dict):
            self._container[key] = AdJson(value)
            return
        
        self._container[key] = value

    
    def _proc_dict_para(self, arg):
        print("proc dict")
        if not isinstance(arg, dict):
            return
        
        for key, value in arg.items():
            self[key] = value
    
    def show(self):
        print(self._container)


