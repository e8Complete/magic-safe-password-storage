import unittest
from password_utils import hash_password, verify_password

class TestPasswordUtils(unittest.TestCase):

    def test_hash_password_returns_bytes(self):
        password = "testpassword"
        # Uses default rounds (12)
        hashed_password = hash_password(password)
        self.assertIsInstance(hashed_password, bytes, "hash_password should return bytes.")

    def test_verify_password_correct_password(self):
        password = "securepassword123"
        # Uses default rounds (12)
        hashed_password = hash_password(password)
        self.assertTrue(verify_password(password, hashed_password), "verify_password should return True for the correct password.")

    def test_verify_password_incorrect_password(self):
        password = "securepassword123"
        # Uses default rounds (12)
        hashed_password = hash_password(password)
        self.assertFalse(verify_password("wrongpassword", hashed_password), "verify_password should return False for an incorrect password.")

    def test_hash_and_verify_integration(self):
        password = "anotherSecurePassword"
        # Uses default rounds (12)
        hashed_password = hash_password(password)
        self.assertIsInstance(hashed_password, bytes, "Hashed password should be bytes.")
        self.assertTrue(verify_password(password, hashed_password), "Verification of correct password failed.")
        self.assertFalse(verify_password("incorrectAttempt", hashed_password), "Verification of incorrect password should return False.")
        
        # Test with an empty password
        empty_password = ""
        # Uses default rounds (12)
        hashed_empty_password = hash_password(empty_password)
        self.assertIsInstance(hashed_empty_password, bytes, "Hashed empty password should be bytes.")
        self.assertTrue(verify_password(empty_password, hashed_empty_password), "Verification of empty password failed.")
        self.assertFalse(verify_password(" ", hashed_empty_password), "Verification of space password against empty hashed password should fail.")

    def test_hash_password_with_custom_rounds(self):
        password = "customRoundsPassword"
        custom_rounds = 4 # Using a low number for faster tests
        
        hashed_password_custom_rounds = hash_password(password, rounds=custom_rounds)
        self.assertIsInstance(hashed_password_custom_rounds, bytes, "Hashed password with custom rounds should be bytes.")
        
        # Verify with the correct password
        self.assertTrue(
            verify_password(password, hashed_password_custom_rounds),
            "verify_password should return True for the correct password with custom rounds hash."
        )
        
        # Verify with an incorrect password
        self.assertFalse(
            verify_password("wrongCustomPassword", hashed_password_custom_rounds),
            "verify_password should return False for an incorrect password with custom rounds hash."
        )

if __name__ == '__main__':
    unittest.main()
