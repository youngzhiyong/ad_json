#coding=utf-8

import json

class AdJson(object):
    _CONTAINER_NAME = "_container"
    _PARENT = "_parent"
    _KEY = "_key"
    def __init__(self, *args, **kwargs):
        self.__dict__[self._CONTAINER_NAME] = {}

        for arg in args:
            if isinstance(arg, dict):
                self._proc_dict(arg)
                continue

            if isinstance(arg, tuple):
                self._proc_tuple(arg)
                continue

            self._proc_generator(arg)

        self._proc_dict(kwargs)
    
    def __repr__(self):
        return repr(self.to_dict())
    
    def __str__(self):
        return str(self.to_dict())

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value
    
    def __delattr__(self, name):
        del self[name]

    def __getitem__(self, key):
        if key not in self._container:
            return self._proc_not_exist_key(key)

        return self._container.get(key)

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            self._container[key] = AdJson(value)
        elif isinstance(value, list):
            self._container[key] = self._proc_list(value)
        else:
            self._container[key] = value

        self._append_to_parent()
    
    def __delitem__(self, key):
        del self._container[key]
    
    def __iter__(self):
        return iter(self._container)

    def __next__(self):
        return next(self._container)

    def items(self):
        return self._container.items()
    
    def values(self):
        return self._container.values()
    
    def to_dict(self):
        result = {}
        for key, value in self._container.items():
            result[key] = value
            if isinstance(value, type(self)):
                result[key] = value.to_dict()

            if isinstance(value, (list, tuple)):
                result[key] = self._to_sequence(value)
            
        return result
    
    def update(self, *args, **kwargs):
        self._update_args(*args)
        self._update_kwargs(**kwargs)
                   
    def _proc_dict(self, arg):
        for key, value in arg.items():
            self[key] = value
    
    def _proc_tuple(self, arg):
        if isinstance(arg[0], tuple):
            return

        self[arg[0]] = arg[1]

    def _proc_generator(self, arg):
        for key, value in iter(arg):
            self[key] = value
    
    def _proc_list(self, value):
        result = [elem for elem in value]
        if all(not isinstance(elem, (dict, tuple, list)) for elem in result):
            return result
        
        for i, elem in enumerate(result):
            if isinstance(elem, list):
                result[i] = self._proc_list(elem)
                continue

            if isinstance(elem, (dict, tuple, list)):
                result[i] = AdJson(elem)
        
        return result
    
    def _proc_not_exist_key(self, key):
        '''
        主要处理在getitem时容器中不存在的key
        ad_json = AdJson()
        ad_json.a.b.c      此时，期望ad_json.to_dict值为{}
        ad_json.a.b.c = 3  此时，期望ad_json.to_dict值为{"a": {"b": {"c": 3}}}

        此函数需要_append_to_parent函数配合处理
        '''

        ad_json = AdJson()
        ad_json.__dict__[AdJson._PARENT] = self
        ad_json.__dict__[AdJson._KEY] = key

        return ad_json
    
    def _append_to_parent(self):
        '''
        主要处理在_proc_not_exist_key函数中添加的key
        ad_json = AdJson()
        ad_json.a.b.c      此时，期望ad_json.to_dict值为{}
        ad_json.a.b.c = 3  此时，期望ad_json.to_dict值为{"a": {"b": {"c": 3}}}
        '''
        
        key = self.__dict__.pop(AdJson._KEY, None)
        parent = self.__dict__.pop(AdJson._PARENT, None)
        if key is None or parent is None:
            return

        parent[key] = self

    def _to_sequence(self, value):
        result = []
        for item in value:
            if isinstance(item, type(self)):
                result.append(item.to_dict())
            else:
                result.append(item)
        return type(value)(result)
    
    def _update_args(self, *args):
        if not args:
            return

        if len(args) > 1:
            raise TypeError()

        if isinstance(args[0], type(self)):
            self._update(args[0].to_dict())
            return

        if isinstance(args[0], dict):
            self._update(args[0])
            return
        
        raise TypeError()
    
    def _update_kwargs(self, **kwargs):
        if kwargs:
            self._update(kwargs)
    
    def _update(self, update_dict):
        for key, value in update_dict.items():
            if hasattr(self, key) and isinstance(self[key], type(self)) and isinstance(value, dict):
                self[key]._update(value)
                continue

            self[key] = value

    def dump(self, fp, *, skipkeys=False, ensure_ascii=True, check_circular=True,
             allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw):
        json.dump(self.to_dict(), fp, skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                  check_circular=check_circular, allow_nan=allow_nan, cls=cls, indent=indent,
                  separators=separators, default=default, sort_keys=sort_keys, **kw)

    def dumps(self, *, skipkeys=False, ensure_ascii=True, check_circular=True,
              allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw):
        return json.dumps(self.to_dict(), skipkeys=sort_keys, ensure_ascii=ensure_ascii, 
                          check_circular=check_circular, allow_nan=allow_nan, cls=cls, indent=indent, 
                          separators=separators, default=default, sort_keys=sort_keys, **kw)
    
    def load(self, fp, *, cls=None, object_hook=None, parse_float=None,
             parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
        self.__init__(json.load(fp, cls=cls, object_hook=object_hook, parse_float=parse_float,
                                parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw))

    def loads(self, s, *, cls=None, object_hook=None, parse_float=None,
              parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
        self.__init__(json.loads(s, cls=cls, object_hook=object_hook, parse_float=parse_float,
                                parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw))
