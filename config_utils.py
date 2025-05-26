import os
from dotenv import load_dotenv

def load_environment_variables(env_path: str | None = None) -> bool:
    """
    Loads environment variables from a .env file.

    Args:
        env_path: Optional path to the .env file. If None, dotenv will
                  try to find a .env file in the current directory or parent directories.

    Returns:
        True if a .env file was loaded, False otherwise.
    """
    # For development, load variables from .env file if it exists.
    # In production, variables should be set directly in the environment.
    # The .env file should be in .gitignore and not committed with sensitive data.
    if env_path:
        return load_dotenv(dotenv_path=env_path, verbose=True)
    return load_dotenv(verbose=True)


def get_app_credential(variable_name: str) -> str | None:
    """
    Retrieves an application credential from an environment variable.

    Args:
        variable_name: The name of the environment variable.

    Returns:
        The value of the environment variable, or None if not found.
    """
    # Load .env file (useful for local development)
    # In a real application, you might call this once at startup.
    # For this example, we call it here for simplicity, but be mindful of repeated calls.
    # A more robust approach might involve a dedicated config loading module/class.
    load_environment_variables() # Ensure .env is loaded (if present)

    return os.getenv(variable_name)

if __name__ == '__main__':
    # Example of how to use it:
    # Create a .env file in the same directory as this script for this example to work:
    # API_KEY="your_actual_api_key"
    # DATABASE_URL="your_actual_database_url"

    print("Attempting to load .env file...")
    if load_environment_variables():
        print(".env file loaded successfully.")
    else:
        print(".env file not found or failed to load. Ensure it exists or environment variables are set directly.")

    api_key = get_app_credential("API_KEY")
    db_url = get_app_credential("DATABASE_URL")
    non_existent_var = get_app_credential("NON_EXISTENT_VAR")

    if api_key:
        print(f"Retrieved API Key: {api_key}")
    else:
        print("API_KEY not found.")

    if db_url:
        print(f"Retrieved Database URL: {db_url}")
    else:
        print("DATABASE_URL not found.")

    if non_existent_var is None:
        print("Correctly determined that NON_EXISTENT_VAR is not set.")
    else:
        print(f"Incorrectly found NON_EXISTENT_VAR: {non_existent_var}")
