# example_usage.py

from password_utils import hash_password, verify_password
from config_utils import get_app_credential, load_environment_variables
from keyring_utils import store_personal_credential, retrieve_personal_credential, delete_personal_credential, DEFAULT_SERVICE_ID
import getpass
import os
import keyring # Added to catch keyring.errors.NoKeyringError as per original intent

def demonstrate_password_hashing():
    print("\n--- Password Hashing (bcrypt) Demonstration ---")
    plain_password = "mySecurePassword123!"
    
    # Hash the password (e.g., during user registration)
    # Using default rounds (12)
    hashed_pw = hash_password(plain_password)
    print(f"Password: '{plain_password}'")
    # Ensure it's bytes before decoding, handle if it's None or not bytes
    hashed_pw_display = hashed_pw.decode('utf-8') if isinstance(hashed_pw, bytes) else str(hashed_pw)
    print(f"Hashed (default rounds): {hashed_pw_display}")

    # Verify the password (e.g., during login)
    is_correct = verify_password(plain_password, hashed_pw)
    print(f"Verification with correct password: {is_correct}")

    is_correct_wrong = verify_password("wrongPassword!", hashed_pw)
    print(f"Verification with incorrect password: {is_correct_wrong}")

    # Example with custom rounds
    hashed_pw_custom_rounds = hash_password(plain_password, rounds=14)
    hashed_pw_custom_display = hashed_pw_custom_rounds.decode('utf-8') if isinstance(hashed_pw_custom_rounds, bytes) else str(hashed_pw_custom_rounds)
    print(f"Hashed (custom rounds=14): {hashed_pw_custom_display}")
    is_correct_custom = verify_password(plain_password, hashed_pw_custom_rounds)
    print(f"Verification (custom rounds) with correct password: {is_correct_custom}")
    print("-" * 30)


def demonstrate_app_credentials():
    print("\n--- Application Credential (Environment Variables) Demonstration ---")
    # Ensure .env is loaded (especially for local dev)
    # Create a .env file in the project root with:
    # API_KEY="your_actual_api_key_from_env"
    # DATABASE_URL="your_db_connection_string_from_env"
    
    # Attempt to load .env (useful if this script is run directly without prior loading)
    # In a larger app, this is usually done once at startup.
    if not os.getenv("API_KEY"): # Check if already loaded
        print("Attempting to load .env file for app credentials demonstration...")
        if load_environment_variables(): # Assuming this function is in config_utils
            print(".env file loaded successfully.")
        else:
            print(".env file not found or failed to load. Please create one or set environment variables manually.")

    api_key = get_app_credential("API_KEY")
    db_url = get_app_credential("DATABASE_URL")
    secret_key = get_app_credential("APP_SECRET_KEY") # Example of another potential credential

    if api_key:
        print(f"Retrieved API Key: {api_key}")
    else:
        print("API_KEY not found. (Is it set in your .env file or environment?)")

    if db_url:
        print(f"Retrieved Database URL: {db_url}")
    else:
        print("DATABASE_URL not found. (Is it set in your .env file or environment?)")
        
    if secret_key:
        print(f"Retrieved App Secret Key: {secret_key}")
    else:
        print("APP_SECRET_KEY not found. (Is it set in your .env file or environment?)")
    print("Note: For this to work, ensure you have a .env file in the project root or have these variables set in your environment.")
    print("Example .env content:")
    print("API_KEY=\"your_actual_api_key_from_env\"")
    print("DATABASE_URL=\"your_db_connection_string_from_env\"")
    print("APP_SECRET_KEY=\"a_super_secret_application_key\"")
    print("-" * 30)


def demonstrate_keyring_credentials():
    print("\n--- Personal Credential (OS Keyring) Demonstration ---")
    service_id = DEFAULT_SERVICE_ID
    try:
        example_username = getpass.getuser() + "_example"
    except Exception:
        example_username = "defaultuser_example_keyring_demo" # Fallback username

    print(f"Using service_id: '{service_id}' and username: '{example_username}'")
    print("You might be prompted by your OS to allow access to the keyring.")
    print("If running in a non-interactive environment, password prompts might be skipped.")

    password_to_store_this_run = None # Flag to track if we attempted to store a password

    try:
        # Check if a credential already exists
        existing_password = retrieve_personal_credential(service_id, example_username)
        if existing_password:
            print(f"A credential for '{example_username}' already exists for service '{service_id}'.")
            try:
                choice = input("Delete existing and create new for demo? (yes/no) [no]: ").lower().strip()
                if choice == 'yes':
                    if not delete_personal_credential(service_id, example_username):
                        print("Failed to delete existing credential. Aborting keyring demo.")
                        print("-" * 30)
                        return
                    print("Existing credential deleted.")
                else:
                    print("Skipping keyring demo as credential exists and user chose not to re-create.")
                    print("-" * 30)
                    return
            except (EOFError, OSError):
                print("Non-interactive environment or input error. Assuming 'no' for deletion. Skipping keyring demo.")
                print("-" * 30)
                return
        
        # Prompt for a password to store
        print("Attempting to get password for keyring storage...")
        password_to_store = getpass.getpass(f"Enter a test password for {example_username}@{service_id} (will be stored in OS keyring): ")
        password_to_store_this_run = password_to_store # Mark that we are attempting to store

        if store_personal_credential(service_id, example_username, password_to_store):
            print("Password stored successfully in keyring.")
            retrieved_password = retrieve_personal_credential(service_id, example_username)
            if retrieved_password:
                print(f"Retrieved password: {'*' * len(retrieved_password)}")
                if retrieved_password == password_to_store:
                    print("SUCCESS: Stored and retrieved passwords match!")
                else:
                    print("ERROR: Stored and retrieved passwords DO NOT match.")
            else:
                print("ERROR: Failed to retrieve password after storing from keyring.")
        else:
            print("Failed to store password in keyring. Check console (e.g., NoKeyringError).")
            print("If 'NoKeyringError', try 'pip install keyrings.alt'.")

    except keyring.errors.NoKeyringError:
        print("Keyring access failed: No keyring backend. Install 'keyrings.alt'.")
    except (EOFError, OSError, getpass.GetPassWarning): # Catch errors if getpass fails
        print("Failed to get password (non-interactive env or getpass issue). Skipping keyring store/retrieve.")
    except Exception as e:
        print(f"An unexpected error in keyring demo: {e}")
    finally:
        # Clean up: delete the credential only if it was set in this interactive session
        if password_to_store_this_run:
            print(f"Cleaning up: deleting credential for {example_username}@{service_id}...")
            if delete_personal_credential(service_id, example_username):
                if retrieve_personal_credential(service_id, example_username) is None:
                    print("Successfully deleted and verified deletion.")
                else:
                    print("Error: Credential still found after attempted deletion.")
            else:
                print("Failed to delete credential. Manual check might be needed.")
        else:
            print("Skipping keyring cleanup as no new password was set for storage in this run.")
    print("-" * 30)


if __name__ == "__main__":
    print("Running demonstrations for secure credential management...")
    
    demonstrate_password_hashing()
    demonstrate_app_credentials()
    demonstrate_keyring_credentials()
    
    print("\nAll demonstrations complete.")
    print("Review output and utility files for details.")
    print("Ensure .env file for app credentials and keyring backend for keyring demo.")
    print("For keyring demo, OS prompts for permissions may occur.")
    print("If keyring ops failed, ensure 'keyrings.alt' is installed and OS keyring is accessible.")
