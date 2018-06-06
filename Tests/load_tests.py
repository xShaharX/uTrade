from locust import HttpLocust, TaskSet, task
import logging

from Tests.credentials import USER_CREDENTIALS


class LoginWithUniqueUsersSteps(TaskSet):
    username = "NOT_FOUND"
    password = "NOT_FOUND"

    def on_start(self):
            if len(USER_CREDENTIALS) > 0:
                self.username, self.password = USER_CREDENTIALS.pop()

    @task
    def login(self):
        self.client.post("/users/login", {
            'username': self.username, 'password': self.password
        })
        logging.info('Login with %s username and %s password', self.username, self.password)


class LoginWithUniqueUsersTest(HttpLocust):
    task_set = LoginWithUniqueUsersSteps
    host = "http://localhost:8000/app"
    sock = None

    def __init__(self):
        super(LoginWithUniqueUsersTest, self).__init__()


if __name__ == '__main__':
    LoginWithUniqueUsersTest().run()
