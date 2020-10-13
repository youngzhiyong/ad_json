#coding=utf-8

import unittest
import json
import os
import sys

sys.path.append("..")
from ad_json import AdJson

class AdJsonTest(unittest.TestCase):
    _test_list = [1, 2, 3]
    _test_json = {'a': {'b': {'c': _test_list}}}

    def assert_ad_json_equal(self, lhd, rhd, msg=None):
        lhd_dict = lhd
        if isinstance(lhd, AdJson):
            lhd_dict = lhd.to_dict()
        
        rhd_dict = rhd
        if isinstance(rhd, AdJson):
            rhd_dict = rhd.to_dict()
        
        self.assertDictEqual(lhd_dict, rhd_dict, msg)

    def test_set_one_level_item(self):
        som_json = {'a': self._test_list}
        ad_json = AdJson()
        ad_json['a'] = self._test_list
        self.assert_ad_json_equal(ad_json, som_json)

    def test_set_two_level_items(self):
        som_json = {'a': {'b': self._test_list}}
        ad_json = AdJson()
        ad_json['a']['b'] = self._test_list
        self.assert_ad_json_equal(ad_json, som_json)

    def test_set_three_level_items(self):
        ad_json = AdJson()
        ad_json['a']['b']['c'] = self._test_list
        self.assert_ad_json_equal(ad_json, self._test_json)

    def test_set_one_level_property(self):
        ad_json = AdJson()
        ad_json.a = self._test_list
        self.assert_ad_json_equal(ad_json, {'a': self._test_list})

    def test_set_two_level_properties(self):
        ad_json = AdJson()
        ad_json.a.b = self._test_list
        self.assert_ad_json_equal(ad_json, {'a': {'b': self._test_list}})

    def test_set_three_level_properties(self):
        ad_json = AdJson()
        ad_json.a.b.c = self._test_list
        self.assert_ad_json_equal(ad_json, self._test_json)

    def test_init_with_dict(self):
        self.assert_ad_json_equal(self._test_json, AdJson(self._test_json))

    def test_init_with_kws(self):
        ad_json = AdJson(a=2, b={'a': 2}, c=[{'a': 2}])
        self.assert_ad_json_equal(ad_json, {'a': 2, 'b': {'a': 2}, 'c': [{'a': 2}]})

    def test_init_with_tuples(self):
        ad_json = AdJson((0, 1), (1, 2), (2, 3))
        self.assert_ad_json_equal(ad_json, {0: 1, 1: 2, 2: 3})

    def test_init_with_list(self):
        ad_json = AdJson([(0, 1), (1, 2), (2, 3)])
        self.assert_ad_json_equal(ad_json, {0: 1, 1: 2, 2: 3})

    def test_init_with_generator(self):
        ad_json = AdJson(((i, i + 1) for i in range(3)))
        self.assert_ad_json_equal(ad_json, {0: 1, 1: 2, 2: 3})

    def test_init_with_tuples_and_empty_list(self):
        ad_json = AdJson((0, 1), [], (2, 3))
        self.assert_ad_json_equal(ad_json, {0: 1, 2: 3})

    def test_init_raises(self):
        def init():
            AdJson(5)

        def init2():
            AdJson('a')
        self.assertRaises(TypeError, init)
        self.assertRaises(ValueError, init2)

    def test_init_with_empty_stuff(self):
        a = AdJson({})
        b = AdJson([])
        self.assert_ad_json_equal(a, {})
        self.assert_ad_json_equal(b, {})

    def test_init_with_list_of_dicts(self):
        a = AdJson({'a': [{'b': 2}]})
        self.assertIsInstance(a.a[0], AdJson)
        self.assertEqual(a.a[0].b, 2)

    def test_init_with_kwargs(self):
        a = AdJson(a='b', c=dict(d='e', f=dict(g='h')))

        self.assertEqual(a.a, 'b')
        self.assertIsInstance(a.c, AdJson)
  
        self.assertEqual(a.c.f.g, 'h')
        self.assertIsInstance(a.c.f, AdJson)

    def test_getitem(self):
        ad_json = AdJson(self._test_json)
        self.assertEqual(ad_json['a']['b']['c'], self._test_list)

    def test_empty_getitem(self):
        ad_json = AdJson()
        ad_json.a.b.c
        self.assert_ad_json_equal(ad_json, {})

    def test_getattr(self):
        ad_json = AdJson(self._test_json)
        self.assertEqual(ad_json.a.b.c, self._test_list)

    def test_str(self):
        ad_json = AdJson(self._test_json)
        self.assertEqual(str(ad_json), str(self._test_json))

    def test_json(self):
        som_json = self._test_json
        some_json = json.dumps(som_json)
        ad_json = AdJson()
        ad_json.a.b.c = self._test_list
        prop_json = json.dumps(ad_json.to_dict())
        self.assertEqual(some_json, prop_json)

    def test_delitem(self):
        ad_json = AdJson({'a': 2})
        del ad_json['a']
        self.assert_ad_json_equal(ad_json, {})

    def test_delitem_nested(self):
        ad_json = AdJson(self._test_json)
        del ad_json['a']['b']['c']
        self.assert_ad_json_equal(ad_json, {'a': {'b': {}}})

    def test_delattr(self):
        ad_json = AdJson({'a': 2})
        del ad_json.a
        self.assert_ad_json_equal(ad_json, {})

    def test_delattr_nested(self):
        ad_json = AdJson(self._test_json)
        del ad_json.a.b.c
        self.assert_ad_json_equal(ad_json, {'a': {'b': {}}})

    def test_delitem_delattr(self):
        ad_json = AdJson(self._test_json)
        del ad_json.a['b']
        self.assert_ad_json_equal(ad_json, {'a': {}})

    def test_tuple_key(self):
        ad_json = AdJson()
        ad_json[(1, 2)] = 2
        self.assert_ad_json_equal(ad_json, {(1, 2): 2})
        self.assertEqual(ad_json[(1, 2)], 2)

    def test_to_dict(self):
        nested = {'a': [{'a': 0}, 2], 'b': {}, 'c': 2}
        ad_json = AdJson(nested)
        regular = ad_json.to_dict()
        self.assert_ad_json_equal(regular, ad_json)
        self.assert_ad_json_equal(regular, nested)
        self.assertNotIsInstance(regular, AdJson)

        def get_attr():
            regular.a = 2
        self.assertRaises(AttributeError, get_attr)

        def get_attr_deep():
            regular['a'][0].a = 1
        self.assertRaises(AttributeError, get_attr_deep)

    def test_to_dict_with_tuple(self):
        nested = {'a': ({'a': 0}, {2: 0})}
        ad_json = AdJson(nested)
        regular = ad_json.to_dict()
        self.assert_ad_json_equal(regular, ad_json)
        self.assert_ad_json_equal(regular, nested)
        self.assertIsInstance(regular['a'], tuple)
        self.assertNotIsInstance(regular['a'][0], AdJson)

    def test_update(self):
        old = AdJson()
        old.child.a = 'a'
        old.child.b = 'b'
        old.foo = 'c'

        new = AdJson()
        new.child.b = 'b2'
        new.child.c = 'c'
        new.foo.bar = True

        old.update(new)

        reference = {'foo': {'bar': True},
                     'child': {'a': 'a', 'c': 'c', 'b': 'b2'}}

        self.assert_ad_json_equal(old, reference)

    def test_update_with_lists(self):
        org = AdJson()
        org.a = [1, 2, {'a': 'superman'}]
        someother = AdJson()
        someother.b = [{'b': 123}]
        org.update(someother)

        correct = {'a': [1, 2, {'a': 'superman'}],
                   'b': [{'b': 123}]}

        org.update(someother)
        self.assert_ad_json_equal(org, correct)
        self.assertIsInstance(org.b[0].to_dict(), dict)

    def test_update_with_kws(self):
        org = AdJson(one=1, two=2)
        someother = AdJson(one=3)
        someother.update(one=1, two=2)
        self.assert_ad_json_equal(org, someother)

    def test_update_with_args_and_kwargs(self):
        expected = {'a': 1, 'b': 2}
        org = AdJson()
        org.update({'a': 3, 'b': 2}, a=1)
        self.assert_ad_json_equal(org, expected)

    def test_update_with_multiple_args(self):
        org = AdJson()
        def update():
            org.update({'a': 2}, {'a': 1})
        self.assertRaises(TypeError, update)

    def test_dict_in_constructor(self):
        ad_dict = AdJson(self._test_json)
        self.assertIsInstance(ad_dict['a'], AdJson)

    def test_init_from_zip(self):
        keys = ['a']
        values = [42]
        items = zip(keys, values)
        d = AdJson(items)
        self.assertEqual(d.a, 42)
    
    def test_json_dump_load(self):
        origin = {'a': [{'a': 0}, 2], 'b': {}, 'c': 2}

        json_file = "test.json"
        with open(json_file, "w", encoding="utf-8") as fp:
            ad_json = AdJson(origin)
            ad_json.dump(fp)
        
        target = None
        with open(json_file, "r", encoding="utf-8") as fp:
            ad_json = AdJson()
            ad_json.load(fp)
            target = ad_json.to_dict()
        
        self.assert_ad_json_equal(origin, target)

        os.remove(json_file)
    
    def test_json_dumps_loads(self):
        origin = {'a': [{'a': 0}, 2], 'b': {}, 'c': 2}

        ad_json = AdJson(origin)
        dumps_result = ad_json.dumps()

        target = AdJson()
        target.loads(dumps_result)

        self.assert_ad_json_equal(origin, target)
    
    def test_zero_key(self):
        ad_json = AdJson()
        ad_json[0].a = 10

        expect = {0: {"a": 10}}
        self.assert_ad_json_equal(ad_json, expect)
    
    def test_items(self):
        origin = {'a': {'a': 0}, 'b': {}, 'c': 2}
        ad_json = AdJson(origin)

        def walk(root, expect):
            if isinstance(root, (list, tuple)):
                for exp, value in zip(expect, root):
                    if isinstance(value, AdJson):
                        walk(value, exp)
                        continue

                    self.assertEqual(value, exp)
                return
            
            for key, value in root.items():
                if isinstance(value, (AdJson, list, tuple)):
                    walk(value, expect[key])
                    continue
                self.assertEqual(value, expect[key])
        
        walk(ad_json, origin)


if __name__ == "__main__":
    unittest.main()
