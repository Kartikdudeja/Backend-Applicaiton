import time, random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):

    wait_time = between(1, 5)

    @task
    def default(self):
        self.client.get("/")

    @task(5)
    def login(self):
        self.client.post("/apigw/login", data={
	"username": "user@mail.com",
	"password": "password"
    })

    @task(2)
    def cache_test(self):

        user_id = str(random.randint(1,17))
        self.client.get(f"/apigw/data/{user_id}")


    def on_start(self):
        with self.client.post("/apigw/login", data={
	"username": "user@mail.com",
	"password": "password"
    }) as response: 

            self.token = response.json().get('access_token')

    @task(10)
    def get_account_details(self):
        self.client.get("/apigw/accounts", headers={"authorization": f"Bearer {self.token}"})