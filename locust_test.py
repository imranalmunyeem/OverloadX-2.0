from locust import HttpUser, task, between, events
import json
import os

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_test(self):
        self.client.get("/")  # Replace with actual endpoint

# Event listener to save results after the test
@events.quitting.add_listener
def save_results(environment, **kwargs):
    stats = []
    for stat in environment.stats.entries.values():
        stats.append({
            "name": stat.name,
            "method": stat.method,
            "num_requests": stat.num_requests,
            "num_failures": stat.num_failures,
            "avg_response_time": stat.avg_response_time if stat.num_requests > 0 else 0,
            "min_response_time": stat.min_response_time if stat.num_requests > 0 else 0,
            "max_response_time": stat.max_response_time if stat.num_requests > 0 else 0,
            "requests_per_second": stat.total_rps
        })

    # Ensure results are saved even if no requests were made
    if not stats:
        stats.append({
            "name": "No Data",
            "method": "N/A",
            "num_requests": 0,
            "num_failures": 0,
            "avg_response_time": 0,
            "min_response_time": 0,
            "max_response_time": 0,
            "requests_per_second": 0
        })

    results_file = "reports/test_results.json"
    os.makedirs(os.path.dirname(results_file), exist_ok=True)

    with open(results_file, "w") as f:
        json.dump(stats, f, indent=4)

    print(f"Results saved to {results_file}")
