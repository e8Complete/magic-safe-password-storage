# Secure Credential Management in Python

## Introduction

Securely managing credentials (like user passwords, API keys, and database connection strings) is crucial for the security and integrity of any application. Storing sensitive information in plain text or using weak hashing mechanisms can lead to severe security breaches. This project demonstrates various techniques for handling different types of credentials securely in Python applications.

## Scenarios Covered

This project provides utilities and examples for three common credential management scenarios:

### 1. User Password Storage (for Login Systems)

*   **Concept:** When storing user passwords for authentication, they must never be stored in plain text. Instead, they should be hashed using a strong, slow, and salted hashing algorithm. `bcrypt` is an excellent choice for this.
    *   **Salting:** `bcrypt` automatically generates a unique salt for each password before hashing. This salt is then stored as part of the resulting hash string. This means that even if two users have the same password, their stored hashes will be different, preventing rainbow table attacks.
    *   **Rounds (Cost Factor):** `bcrypt` allows you to specify a "cost factor" (often called rounds). This determines how computationally intensive the hashing process is. A higher cost factor makes the hashing slower, thus making brute-force attacks more difficult and time-consuming. This value should be chosen carefully to balance security with server performance and can be increased over time as computing power grows.
*   **Implementation:** See `password_utils.py` for functions to hash and verify passwords using `bcrypt`.
*   **Tests:** Unit tests are available in `test_password_utils.py`.

### 2. Application Credentials (API Keys, DB Passwords)

*   **Concept:** Application credentials, such as API keys, database URLs, or external service tokens, should not be hardcoded into the source code or committed to version control. A common practice for local development and some deployment scenarios is to use environment variables, often loaded from a `.env` file.
    *   `python-dotenv` is a library that helps load variables from a `.env` file into the application's environment.
*   **Implementation:** See `config_utils.py` for utilities to load and retrieve credentials from environment variables (potentially sourced from a `.env` file).
*   **Tests & Example:** Unit tests are in `test_config_utils.py`. An example environment file is provided as `.env.example`.
*   **Production Note:** For production environments, using `.env` files might not be sufficiently secure or manageable. It's highly recommended to use dedicated secret management services like:
    *   AWS Secrets Manager
    *   Azure Key Vault
    *   Google Cloud Secret Manager
    *   HashiCorp Vault

### 3. Local Personal Credentials (for Local Scripts/Tools)

*   **Concept:** For scripts or tools running on a local machine that need to access personal credentials (e.g., a script that connects to a personal cloud service), the operating system's keyring service provides a secure way to store and retrieve this information. The `keyring` library in Python provides a cross-platform way to interact with these OS keyrings.
*   **Implementation:** See `keyring_utils.py` for functions to store, retrieve, and delete credentials using the OS keyring.
*   **Tests:** Unit tests using mocking are available in `test_keyring_utils.py`.

## Setup and Installation

1.  **Python Version:** Python 3.8+ is recommended.
2.  **Virtual Environment:** It's highly recommended to create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    Create a `requirements.txt` file (or use the one provided if it exists) with the following content:
    ```
    bcrypt
    python-dotenv
    keyring
    keyrings.alt
    ```
    Then install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *Note on `keyring` backends:* `keyrings.alt` provides common backends. Depending on your OS, you might need others (e.g., `pywin32` on Windows if `keyrings.alt` doesn't suffice, though `keyrings.alt` often includes necessary Windows components or fallbacks).

## How to Run Examples

The `example_usage.py` script demonstrates the functionalities of the different utility modules:

1.  **Password Hashing:** Shows how to hash and verify passwords.
2.  **App Credentials:**
    *   Before running, copy `.env.example` to a new file named `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Edit the `.env` file to replace placeholder values with actual (test) credentials.
    *   The script will then attempt to load these values.
3.  **Keyring Credentials:**
    *   This part of the script will interact with your OS's keyring.
    *   You might be prompted by your operating system to allow access or to enter your system password.
    *   It attempts to store, retrieve, and then delete a test credential.

Run the example script:
```bash
python example_usage.py
```

## Running Tests

To run all unit tests, navigate to the project root directory and use the `unittest` module's discovery feature:
```bash
python -m unittest discover -s . -p "test_*.py"
```
This command will automatically find all files in the current directory (`.`) and its subdirectories that match the pattern `test_*.py`.

## Security Best Practices (Summary)

*   **Never Store Plain Text Passwords:** Always hash passwords for storage.
*   **Hashing is One-Way:** Use strong, one-way hashing algorithms like bcrypt, scrypt, or Argon2. Do not use outdated algorithms like MD5 or SHA1 for passwords.
*   **Salting is Crucial:** Always use a unique salt for each password before hashing. `bcrypt` handles this automatically.
*   **Cost Factor (Rounds):** Configure a sufficiently high cost factor for password hashing to make brute-force attacks computationally expensive.
*   **Use Established Libraries:** Rely on well-vetted, open-source libraries for cryptographic operations (e.g., `bcrypt`, `cryptography`). Do not attempt to invent your own cryptographic algorithms or schemes.
*   **Keep Libraries Updated:** Regularly update your dependencies to patch known vulnerabilities.
*   **HTTPS for Transmission:** Always transmit credentials over HTTPS to protect them in transit.
*   **Strong Password Policies:** Enforce strong password policies for users (length, complexity, uniqueness).
*   **Consider Multi-Factor Authentication (MFA):** Implement MFA for an additional layer of security.
*   **Rate Limiting:** Implement rate limiting on login attempts and other sensitive operations to deter brute-force attacks.
*   **Principle of Least Privilege:** Ensure that applications and users only have access to the credentials and permissions necessary for their tasks.
*   **Regular Security Audits:** Conduct regular security audits and penetration testing to identify and address vulnerabilities.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs, improvements, or feature suggestions.
For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the (optional) `LICENSE` file for details.
