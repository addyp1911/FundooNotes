"""
******************************************************************************
* Purpose: purpose is to show the load testing of API views for debugging and load testing
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""

from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.client.post("/api/login/", {"username": "lal12", "password": "string"})

    @task(1)
    def test_password_reset(self):
        self.client.post('/api/forgot-password/',
                         {"username": "lal12", "email": "addyp1911@gmail.com", "new_password": "hello"})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
