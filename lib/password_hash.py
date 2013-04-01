'''
Created on Jan 1, 2013

@author: Michal Klis
'''
from hasher import HashDirector
import hashlib
import unittest

class PasswordHash():
    def __init__(self):
        self.pass_hash = HashDirector(hash_method = hashlib.sha256)

    def hash_password(self, string):
        (h, salt) = self.pass_hash.make_hash(string)
        return "%s|%s" % (h.hexdigest(), salt)

    def validate_password(self, password, hash_with_salt):
        (h, salt) = hash_with_salt.split('|')
        return self.pass_hash._hash(password, salt).hexdigest() == h

class TestPasswordHash(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.test_string = "This is test!"

    def test_hash(self):
        hash_with_salt = PasswordHash().hash_password(self.test_string)
        self.assertTrue(PasswordHash().validate_password(self.test_string,
                                                            hash_with_salt))