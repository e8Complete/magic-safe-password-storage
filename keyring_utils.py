import keyring
import getpass # For safely getting input if needed for examples

# A generic service name, applications might want to make this more specific
DEFAULT_SERVICE_ID = "my_python_application_credentials"

def store_personal_credential(service_id: str, username: str, password: str) -> bool:
    """
    Stores a personal credential securely in the OS keyring.

    Args:
        service_id: A unique identifier for the service/application storing the credential.
        username: The username associated with the credential.
        password: The password to store.

    Returns:
        True if storing was successful (or if keyring is not available but no error occurred),
        False if an error occurred or keyring is definitively not available.
    """
    try:
        keyring.set_password(service_id, username, password)
        print(f"Credential for '{username}' at '{service_id}' stored successfully in OS keyring.")
        return True
    except keyring.errors.NoKeyringError:
        print("Warning: No keyring backend found. Cannot store password securely in OS keyring.")
        print("Consider installing a backend like 'keyrings.alt' (e.g., pip install keyrings.alt).")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while storing the password: {e}")
        return False

def retrieve_personal_credential(service_id: str, username: str) -> str | None:
    """
    Retrieves a personal credential from the OS keyring.

    Args:
        service_id: The service identifier used when storing the credential.
        username: The username associated with the credential.

    Returns:
        The retrieved password, or None if not found or an error occurred.
    """
    try:
        password = keyring.get_password(service_id, username)
        if password:
            print(f"Credential for '{username}' at '{service_id}' retrieved successfully from OS keyring.")
            return password
        else:
            print(f"No credential found for '{username}' at '{service_id}' in OS keyring.")
            return None
    except keyring.errors.NoKeyringError:
        print("Warning: No keyring backend found. Cannot retrieve password from OS keyring.")
        print("Consider installing a backend like 'keyrings.alt'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while retrieving the password: {e}")
        return None

def delete_personal_credential(service_id: str, username: str) -> bool:
    """
    Deletes a personal credential from the OS keyring.

    Args:
        service_id: The service identifier.
        username: The username.

    Returns:
        True if deletion was successful or if the credential didn't exist.
        False if an error occurred or keyring is not available.
    """
    try:
        keyring.delete_password(service_id, username)
        print(f"Credential for '{username}' at '{service_id}' deleted successfully from OS keyring (if it existed).")
        return True
    except keyring.errors.NoKeyringError:
        print("Warning: No keyring backend found. Cannot delete password from OS keyring.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while deleting the password: {e}")
        return False

if __name__ == '__main__':
    # This example demonstrates basic usage.
    # In a real application, you might get the username via getpass.getuser() or a config.
    # Password input should always use getpass.getpass() for security.

    service = DEFAULT_SERVICE_ID
    test_user = "testuser_keyring_example"

    print("\n--- Keyring Example ---")
    # Prompt for password for storage
    # Note: For automated scripts, you wouldn't typically prompt.
    # This is for interactive demonstration.
    print(f"Running keyring example for service '{service}' and user '{test_user}'.")
    print("You might be prompted by your OS to allow access to the keyring.")

    try:
        # In a non-interactive environment (like this script), getpass.getpass might not work.
        # We'll use a default password for the example to run in automation.
        # In a real interactive script, getpass.getpass() is the way to go.
        password_to_store = "test_password_123"
        print(f"Using a default password for '{test_user}@{service}' for this non-interactive example.")
        # password_to_store = getpass.getpass(f"Enter a test password for {test_user}@{service} (will be stored in OS keyring): ")
        
        if store_personal_credential(service, test_user, password_to_store):
            retrieved_pw = retrieve_personal_credential(service, test_user)
            if retrieved_pw:
                print(f"Retrieved: {'*' * len(retrieved_pw)}") # Avoid printing the actual password
                if retrieved_pw == password_to_store:
                    print("Successfully stored and retrieved the test password.")
                else:
                    print("Error: Retrieved password does not match the stored one.")
            else:
                print("Failed to retrieve password after storing.")

            # Clean up: delete the test credential
            print(f"Attempting to delete credential for {test_user}@{service}...")
            if delete_personal_credential(service, test_user):
                # Verify deletion
                if retrieve_personal_credential(service, test_user) is None:
                    print(f"Successfully deleted and verified deletion of {test_user}@{service}.")
                else:
                    print(f"Error: Credential for {test_user}@{service} still found after attempting deletion.")
            else:
                print(f"Failed to delete credential for {test_user}@{service}.")

        else:
            print("Failed to store password. Keyring might not be available or configured.")
            print("Try 'pip install keyrings.alt' if you see 'NoKeyringError'.")

    except Exception as e:
        print(f"An error occurred during the keyring example: {e}")
        print("This could be due to issues with the OS keyring or lack of a backend.")
        print("Ensure a keyring backend is installed (e.g., 'keyrings.alt' on Linux/macOS, 'pywin32' on Windows).")
