import hashlib, binascii, os

class BasicAuth(object):
  def __init__(self, auth_dict):
    self.auth_dict = auth_dict
 

  @staticmethod
  def hash_password(password):
      salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
      pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
      pwdhash = binascii.hexlify(pwdhash)
      return (salt + pwdhash).decode('ascii')
 

  def _verify_password(self, username, provided_password):
      if username not in self.auth_dict:
        return False
      stored_password = self.auth_dict[username]
      salt = stored_password[:64]
      stored_password = stored_password[64:]
      pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
      pwdhash = binascii.hexlify(pwdhash).decode('ascii')
      return pwdhash == stored_password


  def checkpassword(self, realm, user, password):
      return self._verify_password(user, password)

