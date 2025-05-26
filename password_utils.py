import bcrypt

def hash_password(password: str) -> bytes:
  """Hashes a password using bcrypt.

  Args:
    password: The plain-text password to hash.

  Returns:
    The hashed password as bytes.
  """
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
  return hashed_password

def verify_password(password: str, hashed_password: bytes) -> bool:
  """Verifies a password against a bcrypt hash.

  Args:
    password: The plain-text password to verify.
    hashed_password: The bcrypt hashed password (bytes).

  Returns:
    True if the password matches the hash, False otherwise.
  """
  return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
