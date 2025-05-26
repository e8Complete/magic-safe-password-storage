import bcrypt

def hash_password(password: str, rounds: int = 12) -> bytes:
  """Hashes a password using bcrypt.

  bcrypt is a strong hashing algorithm designed to be slow and computationally intensive,
  making it resistant to brute-force attacks.

  Args:
    password: The plain-text password to hash.
    rounds: The computational cost factor for bcrypt. Higher numbers increase
            the hashing time and security. Default is 12.

  Returns:
    The hashed password as bytes.
  """
  # bcrypt.gensalt() automatically generates a unique salt for each password.
  # This salt is then stored as part of the hash itself.
  # The 'rounds' parameter controls the computational cost (work factor) of the hashing.
  # A higher number of rounds means more iterations and thus a slower hash,
  # making it more resistant to brute-force attacks.
  salt = bcrypt.gensalt(rounds=rounds)

  # The password must be encoded to bytes (e.g., UTF-8) before hashing,
  # as cryptographic functions operate on bytes.
  password_bytes = password.encode('utf-8')

  hashed_password = bcrypt.hashpw(password_bytes, salt)
  return hashed_password

def verify_password(password: str, hashed_password: bytes) -> bool:
  """Verifies a password against a bcrypt hash.

  Args:
    password: The plain-text password to verify.
    hashed_password: The bcrypt hashed password (bytes), which includes the salt.

  Returns:
    True if the password matches the hash, False otherwise.
  """
  # The password to check must also be encoded to bytes.
  password_bytes = password.encode('utf-8')

  # bcrypt.checkpw automatically extracts the salt from the stored 'hashed_password'
  # and uses it to hash the provided 'password' for comparison.
  # This means you don't need to store or manage the salt separately.
  return bcrypt.checkpw(password_bytes, hashed_password)
