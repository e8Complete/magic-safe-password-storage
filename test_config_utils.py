import unittest
from unittest import mock
import os
from config_utils import load_environment_variables, get_app_credential

# Use a consistent test .env filename
TEST_ENV_FILE = ".test.env"

class TestConfigUtils(unittest.TestCase):

    def setUp(self):
        # Ensure a clean environment before each test
        self.env_patchers = []
        # Clear relevant environment variables that might be set externally
        # Storing original values to restore them in tearDown
        self.original_env_values = {}
        keys_to_manage = ["TEST_API_KEY", "TEST_DB_URL", "API_KEY", "DATABASE_URL", "EXISTING_VAR", "FILE_VAR_KEY", "NON_EXISTENT_CREDENTIAL"]

        for key in keys_to_manage:
            if key in os.environ:
                self.original_env_values[key] = os.environ[key]
                del os.environ[key] # Direct removal for clean state
            else:
                self.original_env_values[key] = None
        
        # The following logic for patchers in setUp is kept as per the problem description's structure,
        # but direct modification (above) is often simpler for setUp.
        # If the intention was to mock os.environ broadly for each test, @mock.patch.dict(os.environ, {}, clear=True)
        # at the method level is more standard.
        for key in ["TEST_API_KEY", "TEST_DB_URL", "API_KEY", "DATABASE_URL"]: # Reduced list as per original problem desc for this loop
            if key in os.environ: # This condition will be false due to prior deletion
                # This patcher logic in setUp is unusual. Typically, you'd patch os.environ for the whole test
                # or not patch it here if you're directly modifying os.environ for setup.
                # For the sake of following the structure:
                patcher = mock.patch.dict(os.environ, {}, clear=True) # This clears entire os.environ
                # patcher.start() # Starting it here would affect subsequent key checks and os.environ state
                self.env_patchers.append(patcher) 
                # Re-deleting here because clear=True wipes everything, so the specific key removal isn't the main effect.
                # if key in os.environ: del os.environ[key] 

        # Create a dummy .test.env file for testing load_environment_variables
        with open(TEST_ENV_FILE, "w") as f:
            f.write("TEST_API_KEY=dummy_api_key_from_file\n")
            f.write("TEST_DB_URL=dummy_db_url_from_file\n")

    def tearDown(self):
        # Stop all patchers
        for patcher in self.env_patchers:
            try:
                patcher.stop()
            except RuntimeError: # Can happen if patcher wasn't started
                pass
        self.env_patchers.clear()
        
        # Clean up the dummy .test.env file
        if os.path.exists(TEST_ENV_FILE):
            os.remove(TEST_ENV_FILE)
        
        # Restore original environment variables
        for key, value in self.original_env_values.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ: # If it was None originally and set by test, remove it
                del os.environ[key]


    @mock.patch.dict(os.environ, {}, clear=True) # Start with a completely clean os.environ for this test
    def test_load_environment_variables_from_file(self):
        self.assertNotIn("TEST_API_KEY", os.environ)
        self.assertNotIn("TEST_DB_URL", os.environ)

        loaded = load_environment_variables(env_path=TEST_ENV_FILE)
        self.assertTrue(loaded)
        self.assertEqual(os.getenv("TEST_API_KEY"), "dummy_api_key_from_file")
        self.assertEqual(os.getenv("TEST_DB_URL"), "dummy_db_url_from_file")

        # Clean up environment variables set by load_dotenv for isolation
        if "TEST_API_KEY" in os.environ: del os.environ["TEST_API_KEY"]
        if "TEST_DB_URL" in os.environ: del os.environ["TEST_DB_URL"]


    @mock.patch.dict(os.environ, {}, clear=True)
    def test_load_environment_variables_file_not_found(self):
        loaded = load_environment_variables(env_path=".nonexistent.env")
        self.assertFalse(loaded)


    @mock.patch.dict(os.environ, {"EXISTING_VAR": "pre_existing_value"}, clear=True)
    def test_get_app_credential_already_in_env(self):
        with mock.patch("config_utils.load_dotenv") as mock_load_dotenv:
            mock_load_dotenv.return_value = False # Simulate .env not found or not loaded
            retrieved_value = get_app_credential("EXISTING_VAR")
            self.assertEqual(retrieved_value, "pre_existing_value")
            mock_load_dotenv.assert_called_once() 


    @mock.patch.dict(os.environ, {}, clear=True) 
    @mock.patch("config_utils.load_dotenv") 
    def test_get_app_credential_from_loaded_env_file(self, mock_load_dotenv_global):
        def side_effect_load_dotenv(*args, **kwargs):
            os.environ["FILE_VAR_KEY"] = "value_from_mocked_load_dotenv"
            return True 
        
        mock_load_dotenv_global.side_effect = side_effect_load_dotenv

        retrieved_value = get_app_credential("FILE_VAR_KEY")
        self.assertEqual(retrieved_value, "value_from_mocked_load_dotenv")
        mock_load_dotenv_global.assert_called_once() 

        if "FILE_VAR_KEY" in os.environ:
            del os.environ["FILE_VAR_KEY"]


    @mock.patch.dict(os.environ, {}, clear=True)
    @mock.patch("config_utils.load_dotenv", return_value=False) 
    def test_get_app_credential_not_found(self, mock_load_dotenv_global):
        retrieved_value = get_app_credential("NON_EXISTENT_CREDENTIAL")
        self.assertIsNone(retrieved_value)
        mock_load_dotenv_global.assert_called_once()


    def test_load_environment_variables_no_file_present(self):
        disabled_test_env_path = None
        if os.path.exists(TEST_ENV_FILE):
            disabled_test_env_path = TEST_ENV_FILE + ".disabled"
            os.rename(TEST_ENV_FILE, disabled_test_env_path)
        
        # Ensure no actual .env is present either
        actual_env_path = ".env"
        disabled_actual_env_path = None
        if os.path.exists(actual_env_path):
            disabled_actual_env_path = actual_env_path + ".disabled_for_test"
            os.rename(actual_env_path, disabled_actual_env_path)

        try:
            # Mock find_dotenv which is used by python-dotenv's load_dotenv
            with mock.patch('dotenv.main.find_dotenv') as mock_find_dotenv:
                mock_find_dotenv.return_value = "" # Simulate no .env file found

                loaded = load_environment_variables() 
                self.assertFalse(loaded, "load_environment_variables should return False when no .env file is found by find_dotenv.")
        finally:
            if disabled_test_env_path and os.path.exists(disabled_test_env_path):
                os.rename(disabled_test_env_path, TEST_ENV_FILE)
            if disabled_actual_env_path and os.path.exists(disabled_actual_env_path):
                os.rename(disabled_actual_env_path, actual_env_path)


if __name__ == "__main__":
    unittest.main()

```
