from locust import HttpUser, task, between
import random
import string

class WalletUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1 and 3 seconds between tasks

    # List of CBU data for testing
    cbu_data = [
        ("1234567890123456789012", 50000.0),
        ("2345678901234567890123", 75000.0),
        ("3456789012345678901234", 100000.0),
        ("4567890123456789012345", 25000.0),
        ("5678901234567890123456", 150000.0),
        ("6789012345678901234567", 30000.0),
        ("7890123456789012345678", 45000.0),
        ("8901234567890123456789", 60000.0),
        ("9012345678901234567890", 80000.0),
        ("0123456789012345678901", 120000.0),
    ]

    def generate_random_email(self):
        """Generate a random email for testing"""
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{username}@test.com"

    def on_start(self):
        """Execute at the start of each virtual user"""
        # Register a user for testing
        self.email = self.generate_random_email()
        self.password = "password123"

        response = self.client.post(
            "/users/register",
            json={
                "email": self.email,
                "password": self.password
            }
        )

        if response.status_code != 200:
            print(f"Error registering user: {response.text}")

    @task(3)  # Weight 3: more frequent
    def check_balance(self):
        """Check balance"""
        self.client.get(f"/wallet/balance?email={self.email}")

    @task(2)  # Weight 2: medium frequency
    def view_transactions(self):
        """View transactions"""
        self.client.get(f"/transactions?email={self.email}")

    @task(1)  # Weight 1: less frequent
    def transfer_money(self):
        """Transfer money"""
        # Generate a random email for the receiver
        receiver_email = self.generate_random_email()
        amount = random.uniform(100, 1000)  # Random amount between 100 and 1000

        self.client.post(
            "/wallet/transfer",
            json={
                "senderEmail": self.email,
                "receiverEmail": receiver_email,
                "amount": amount
            }
        )

    @task(1)  # Weight 1: less frequent
    def instant_debit(self):
        """Instant debit"""
        #amount = random.uniform(1000, 5000)  # Random amount between 1000 and 5000
        cbu, max_amount = random.choice(self.cbu_data)
        amount = random.uniform(1000, min(5000, max_amount))  # máximo de 5000 o el permitido por ese CBU
        self.client.post(
            "/wallet/instant-debit",
            json={
                "receiverEmail": self.email,
                "bankName": "BBVA",
                "cbu": cbu,
                "amount": amount
            }
        )

    @task(1)  # Weight 1: less frequent
    def login(self):
        """Try login"""
        self.client.post(
            "/users/login",
            json={
                "email": self.email,
                "password": self.password
            }
        )