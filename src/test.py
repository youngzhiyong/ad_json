#coding=utf-8
import unittest
from ad_json import AdJson

class PyJsonTest(unittest.TestCase):
    def test_construct_dict(self):
        ad_json = AdJson({"a": {"b": 3}})
        self.assertEqual(ad_json.a.b, 3)
    
    def test_construct_list(self):
        ad_json = AdJson([{"a": [1, 2]}])
        self.assertEqual(ad_json.a, [1, 2])
    
    def test_construct_tuple(self):
        ad_json = AdJson(({"a": [1, 2]}, 3))
        self.assertEqual(ad_json.a, [1, 2])

    def test_keyword(self):
        ad_json = AdJson(a=2, b=3)
        self.assertEqual(ad_json.a, 2)
        self.assertEqual(ad_json.b, 3)

    
    def test_temp(self):
        ad_json = AdJson()
        ad_json.a = 3
        ad_json["b"] = 5
        print(ad_json.c)
        ad_json.show()


if __name__ == "__main__":
    unittest.main()