import unittest
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE =  re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class UserValidationFailed(Exception):
    pass

class WrongUserName(UserValidationFailed):
    pass

class WrongPassword(UserValidationFailed):
    pass

class PasswordMismatch(WrongPassword):
    pass

class PasswordNotValid(WrongPassword):
    pass

class WrongEmail(UserValidationFailed):
    pass

class UserValidation:
    def __init__(self, autovalidate = True, exceptions = True):
        self.name = ''
        self.password = ''
        self.password2 = ''
        self.email = ''
        self.autovalidate = autovalidate
        self.exceptions = exceptions

    def createUser(self, **userargs):
        self.name = userargs.get('name')
        self.password = userargs.get('password')
        self.password2 = userargs.get('password2')
        self.email = userargs.get('email')

        if self.autovalidate:
            self.validate_user_name()
            self.validate_password()
            self.validate_email()

    def validate_user_name(self):
        if not self.name or not USER_RE.match(self.name):
            if self.exceptions:
                raise WrongUserName
            else:
                return False
        return True

    def validate_password(self):
        if self.password != self.password2:
            if self.exceptions:
                raise PasswordMismatch
            else:
                return False, True
        elif not self.password or not PASSWORD_RE.match(self.password):
            if self.exceptions:
                raise PasswordNotValid
            else:
                return False, False

        return True, True

    def validate_email(self):
        if self.email and not EMAIL_RE.match(self.email):
            if self.exceptions:
                raise WrongEmail
            else:
                return False
        return True

    def getName(self):
        return self.name

class TestUser(unittest.TestCase, UserValidation):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.name = 'lasjdlasdj'
        self.password = 'hdhdhdhd'
        self.email = 'sjd@mmd.com'
        self.somebody = UserValidation()
        self.somebody.createUser(name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)

    def test_create_user(self):
        assert self.somebody

    def test_get_name(self):
        self.assertEquals(self.somebody.getName(), self.name)

    def test_validation(self):
        if __name__ == "udacityuser":
            from mock import Mock

        self.somebody.validate_email = Mock(return_value = None)
        self.somebody.validate_password = Mock(return_value = None)
        self.somebody.validate_user_name = Mock(return_value = None)

        self.somebody.createUser(name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)

        self.assertEqual(self.somebody.validate_email.call_count, 1)
        self.assertEqual(self.somebody.validate_password.call_count, 1)
        self.assertEqual(self.somebody.validate_user_name.call_count, 1)

    def test_password_mismatch(self):
        self.assertRaises(PasswordMismatch, self.somebody.createUser, name = self.name, password = self.password,
                           password2 = self.password + "dfdf", email = self.email)

    def test_wrong_username(self):
        """spaces not allowed"""
        self.assertRaises(WrongUserName, self.somebody.createUser, name = "kk kk", password = self.password,
                                 password2 = self.password, email = self.email)

    def test_wrong_password(self):
        """password too short"""
        self.password = "ab"
        self.assertRaises(PasswordNotValid, self.somebody.createUser, name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)
        """password too long"""
        self.password = "absdjkfklfjsfkjdlkfjsdkljfdklsdjsdflkjsdfsdfsdfsdfsdf"
        self.assertRaises(PasswordNotValid, self.somebody.createUser, name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)

    def test_wrong_email(self):
        """email defined but wrong"""
        self.email = "skdjksdjs"
        self.assertRaises(WrongEmail, self.somebody.createUser, name = self.name, password = self.password,
                            password2 = self.password, email = self.email)

        self.email = "skdj@ksdjs"
        self.assertRaises(WrongEmail, self.somebody.createUser, name = self.name, password = self.password,
                            password2 = self.password, email = self.email)

    def test_empty_email(self):
        self.email = ''

        self.somebody.createUser(name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)

class TestNoExceptionsUser(unittest.TestCase, UserValidation):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.name = 'lasjdlasdj'
        self.password = 'hdhdhdhd'
        self.email = 'sjd@mmd.com'
        self.somebody = UserValidation(False, False)
        self.somebody.createUser(name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)

    def test_password_mismatch(self):
        self.somebody.createUser(name = self.name, password = self.password,
                           password2 = self.password + "dfdf", email = self.email)
        self.assertEquals(self.somebody.validate_password(), (False, True))

    def test_password_match(self):
        self.assertEquals(self.somebody.validate_password(), (True, True))


    def test_wrong_username(self):
        """spaces not allowed"""
        self.somebody.createUser(name = "kk kk", password = self.password,
                                 password2 = self.password, email = self.email)
        self.assertEquals(self.somebody.validate_user_name(), False)

    def test_wrong_password(self):
        """password too short"""
        self.password = "ab"
        self.somebody.createUser(name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)
        self.assertEquals(self.somebody.validate_password(), (False, False))

        """password too long"""
        self.password = "absdjkfklfjsfkjdlkfjsdkljfdklsdjsdflkjsdfsdfsdfsdfsdf"
        self.somebody.createUser(name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)
        self.assertEquals(self.somebody.validate_password(), (False, False))

    def test_wrong_email(self):
        """email defined but wrong"""
        self.email = "skdjksdjs"
        self.somebody.createUser( name = self.name, password = self.password,
                            password2 = self.password, email = self.email)
        self.assertEquals(self.somebody.validate_email(), (False))

        self.email = "skdj@ksdjs"
        self.somebody.createUser(name = self.name, password = self.password,
                            password2 = self.password, email = self.email)
        self.assertEquals(self.somebody.validate_email(), (False))

    def test_empty_email(self):
        self.email = ''

        self.somebody.createUser(name = self.name, password = self.password,
                                 password2 = self.password, email = self.email)
        self.assertEquals(self.somebody.validate_email(), (True))

