import unittest
from unittest import mock
# Make sure keyring is importable, even if it's just for mocking its errors
try:
    import keyring.errors
except ImportError:
    # Create a dummy error class if keyring or its errors are not truly installed,
    # allowing tests to define behavior for this error.
    class MockKeyringError(Exception): pass
    class MockNoKeyringError(MockKeyringError): pass
    keyring = mock.Mock() # Mock the keyring module itself
    keyring.errors = mock.Mock()
    keyring.errors.NoKeyringError = MockNoKeyringError
    keyring.errors.KeyringError = MockKeyringError


from keyring_utils import (
    store_personal_credential,
    retrieve_personal_credential,
    delete_personal_credential,
    DEFAULT_SERVICE_ID
)

# Test constants
TEST_SERVICE = "test_service_id"
TEST_USERNAME = "test_user"
TEST_PASSWORD = "test_password123"

class TestKeyringUtils(unittest.TestCase):

    @mock.patch('keyring_utils.keyring') # Mock the keyring module used by keyring_utils
    def test_store_personal_credential_success(self, mock_keyring_module):
        mock_keyring_module.set_password.return_value = None # Simulate success
        
        result = store_personal_credential(TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD)
        
        self.assertTrue(result)
        mock_keyring_module.set_password.assert_called_once_with(TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD)

    @mock.patch('keyring_utils.keyring')
    def test_store_personal_credential_no_keyring_error(self, mock_keyring_module):
        mock_keyring_module.set_password.side_effect = keyring.errors.NoKeyringError("No backend")
        
        result = store_personal_credential(TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD)
        
        self.assertFalse(result)
        mock_keyring_module.set_password.assert_called_once_with(TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD)

    @mock.patch('keyring_utils.keyring')
    def test_store_personal_credential_other_exception(self, mock_keyring_module):
        mock_keyring_module.set_password.side_effect = Exception("Some other error")
        
        result = store_personal_credential(TEST_SERVICE, TEST_USERNAME, TEST_PASSWORD)
        
        self.assertFalse(result)

    @mock.patch('keyring_utils.keyring')
    def test_retrieve_personal_credential_success(self, mock_keyring_module):
        mock_keyring_module.get_password.return_value = TEST_PASSWORD
        
        password = retrieve_personal_credential(TEST_SERVICE, TEST_USERNAME)
        
        self.assertEqual(password, TEST_PASSWORD)
        mock_keyring_module.get_password.assert_called_once_with(TEST_SERVICE, TEST_USERNAME)

    @mock.patch('keyring_utils.keyring')
    def test_retrieve_personal_credential_not_found(self, mock_keyring_module):
        mock_keyring_module.get_password.return_value = None
        
        password = retrieve_personal_credential(TEST_SERVICE, TEST_USERNAME)
        
        self.assertIsNone(password)

    @mock.patch('keyring_utils.keyring')
    def test_retrieve_personal_credential_no_keyring_error(self, mock_keyring_module):
        mock_keyring_module.get_password.side_effect = keyring.errors.NoKeyringError("No backend")
        
        password = retrieve_personal_credential(TEST_SERVICE, TEST_USERNAME)
        
        self.assertIsNone(password)

    @mock.patch('keyring_utils.keyring')
    def test_retrieve_personal_credential_other_exception(self, mock_keyring_module):
        mock_keyring_module.get_password.side_effect = Exception("Some other error")
        
        password = retrieve_personal_credential(TEST_SERVICE, TEST_USERNAME)
        
        self.assertIsNone(password)

    @mock.patch('keyring_utils.keyring')
    def test_delete_personal_credential_success(self, mock_keyring_module):
        mock_keyring_module.delete_password.return_value = None # Simulate success
        
        result = delete_personal_credential(TEST_SERVICE, TEST_USERNAME)
        
        self.assertTrue(result)
        mock_keyring_module.delete_password.assert_called_once_with(TEST_SERVICE, TEST_USERNAME)

    @mock.patch('keyring_utils.keyring')
    def test_delete_personal_credential_no_keyring_error(self, mock_keyring_module):
        mock_keyring_module.delete_password.side_effect = keyring.errors.NoKeyringError("No backend")
        
        result = delete_personal_credential(TEST_SERVICE, TEST_USERNAME)
        
        self.assertFalse(result)

    @mock.patch('keyring_utils.keyring')
    def test_delete_personal_credential_other_exception(self, mock_keyring_module):
        # Simulate an exception that is not NoKeyringError but occurs during delete_password
        # For example, some backends might raise a generic KeyringError or OSError.
        # We can use keyring.errors.KeyringError if it's available from the import,
        # or a generic Exception if not.
        error_to_raise = keyring.errors.KeyringError if hasattr(keyring.errors, 'KeyringError') and keyring.errors.KeyringError is not keyring.errors.NoKeyringError else Exception
        mock_keyring_module.delete_password.side_effect = error_to_raise("Deletion failed")
        
        result = delete_personal_credential(TEST_SERVICE, TEST_USERNAME)
        
        self.assertFalse(result)
        
    @mock.patch('keyring_utils.keyring')
    def test_default_service_id_usage(self, mock_keyring_module):
        # This test is more of an integration check for the constant,
        # ensuring it's passed if no service_id is given to a hypothetical function.
        # Our current functions require service_id, so we test them with DEFAULT_SERVICE_ID.
        
        mock_keyring_module.get_password.return_value = TEST_PASSWORD
        password = retrieve_personal_credential(DEFAULT_SERVICE_ID, TEST_USERNAME)
        self.assertEqual(password, TEST_PASSWORD)
        mock_keyring_module.get_password.assert_called_with(DEFAULT_SERVICE_ID, TEST_USERNAME)

if __name__ == "__main__":
    unittest.main()
```
