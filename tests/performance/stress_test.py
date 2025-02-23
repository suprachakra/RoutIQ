"""
Stress and load testing scripts for performance validation.
This file is designed to be run with Locust to simulate high load on key endpoints.
"""

from locust import HttpUser, task, between

class FleetOptimizationUser(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def test_health(self):
        self.client.get("/health")

    @task(1)
    def test_sample_data(self):
        self.client.get("/api/data")
