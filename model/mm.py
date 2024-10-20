import hashlib

# User class to store user data
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self._hash_password(password)
        self.secret_key = None

    def _hash_password(self, password):
        # Hash the password for security
        return hashlib.sha256(password.encode()).hexdigest()

    def set_secret_key(self, secret_key):
        # Set the secret key for password reset
        self.secret_key = hashlib.sha256(secret_key.encode()).hexdigest()

    def reset_password(self, new_password, secret_key):
        # Reset password if secret key matches
        if hashlib.sha256(secret_key.encode()).hexdigest() == self.secret_key:
            self.password = self._hash_password(new_password)
            self.secret_key = None
            print("Password reset successful!")
        else:
            print("Incorrect secret key. Password reset failed.")

# Authentication class to handle signup, login, and password reset
class Authentication:
    def __init__(self):
        self.users = {}

    def signup(self, username, password):
        # Register a new user
        if username not in self.users:
            new_user = User(username, password)
            self.users[username] = new_user
            print("Signup successful!")
        else:
            print("Username already taken. Signup failed.")

    def login(self, username, password):
        # Log in an existing user
        if username in self.users:
            user = self.users[username]
            if user.password == hashlib.sha256(password.encode()).hexdigest():
                print("Login successful!")
            else:
                print("Incorrect password. Login failed.")
        else:
            print("Username not found. Login failed.")

    def forgot_password(self, username, secret_key, new_password):
        # Reset password for a user with secret key authentication
        if username in self.users:
            user = self.users[username]
            user.reset_password(new_password, secret_key)
        else:
            print("Username not found. Password reset failed.")

# Usage example
auth = Authentication()

# Signup a new user
auth.signup("user1", "password123")

# Login with correct password
auth.login("user1", "password123")

# Login with incorrect password
auth.login("user1", "wrong_password")

# Set secret key for password reset
user = auth.users["user1"]
user.set_secret_key("secret123")

# Reset password with correct secret key
auth.forgot_password("user1", "secret123", "new_password")

# Reset password with incorrect secret key
auth.forgot_password("user1", "wrong_secret", "new_password")
