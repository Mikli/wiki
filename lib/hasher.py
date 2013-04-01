'''
Created on Dec 31, 2012

@author: Michal Klis
'''
import unittest
import random
import string

class HashDirector():
    def __init__(self, **kwargs):
        self.on_create(**kwargs)

    def on_create(self, **kwargs):
        self.hash_method = kwargs.get('hash_method')

    def _hash(self, string, salt = None):
        s = ""
        if salt:
            s = string + salt
        else:
            s = string
        return self.hash_method(s)

    def _make_salt(self):
        return ''.join(random.choice(string.letters) for x in xrange(5))

    def make_hash(self, string):
        salt = self._make_salt()
        h = self._hash(string, salt)
        return (h, salt)

    def validate_hash(self, string, h, salt):
        return self._hash(string, salt) == h


class TestHash(unittest.TestCase, HashDirector):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.hash1 = 94854908
        self.test_string = "my_string"
        self.hash_method = lambda x: self.hash1

    def test_hash(self):
        self.assertEqual(self._hash(self.test_string), self.hash1)

    def test_making_salt(self):
        self.assertNotEqual(self._make_salt(), self._make_salt())
        self.assertNotEqual(self._make_salt(), self._make_salt())
        self.assertNotEqual(self._make_salt(), self._make_salt())

    def test_making_hash(self):
        (h, salt) = self.make_hash("to_be_tested")
        self.assertIsNotNone(h)
        self.assertIsNotNone(salt)

    def test_validation(self):
        test_string = "to_be_tested"
        (h, salt) = self.make_hash(test_string)
        self.assertEqual(self.validate_hash(test_string, h, salt), True)
