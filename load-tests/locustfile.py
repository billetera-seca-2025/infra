from locust import HttpUser, task, between
import random
import string
import time

registered_emails = []

class WalletUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo entre tareas

    def generate_random_email(self):
        """Genera un email aleatorio"""
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{username}@test.com"

    def on_start(self):
        """Se ejecuta al arrancar cada usuario virtual"""
        self.email = self.generate_random_email()
        self.password = "password123"

        for attempt in range(5):
            try:
                response = self.client.post(
                    "/users/register",
                    json={"email": self.email, "password": self.password},
                    name="/users/register"
                )
                if response.status_code == 200:
                    print(f"Usuario registrado: {self.email}")
                    registered_emails.append(self.email)
                    return
                else:
                    print(f"Error registrando usuario: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error de conexión: {e}")

            time.sleep(3)  # Espera antes de reintentar

        print("Fallo al registrar usuario tras 5 intentos")

    @task(3)
    def check_balance(self):
        self.client.get(
            f"/wallet/balance?email={self.email}",
            name="/wallet/balance"
        )

    @task(2)
    def view_transactions(self):
        self.client.get(
            f"/transactions?email={self.email}",
            name="/transactions"
        )

    @task(1)
    def transfer_money(self):
        if not registered_emails:
            return

        receiver_email = random.choice(registered_emails)
        if receiver_email == self.email:
            return  # No te transfieras a vos mismo

        amount = round(random.uniform(100, 1000), 2)
        response = self.client.post(
            "/wallet/transfer",
            json={
                "senderEmail": self.email,
                "receiverEmail": receiver_email,
                "amount": amount
            },
            name="/wallet/transfer"
        )

        if response.status_code >= 400:
            print(f"[TRANSFER] Error esperado o sin saldo: {response.status_code}")

    @task(1)
    def instant_debit(self):
        amount = round(random.uniform(1000, 5000), 2)
        response = self.client.post(
            "/wallet/instant-debit",
            json={
                "receiverEmail": self.email,
                "bankName": "BBVA",
                "cbu": "4567890123456789012345",
                "amount": amount
            },
            name="/wallet/instant-debit"
        )

        if response.status_code >= 400:
            print(f"[DEBIT] Error esperado o sin saldo: {response.status_code}")

    @task(1)
    def login(self):
        self.client.post(
            "/users/login",
            json={
                "email": self.email,
                "password": self.password
            },
            name="/users/login"
        )
