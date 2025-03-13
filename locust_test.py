from locust import HttpUser, task, between, events
import pandas as pd
import os

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_test(self):
        self.client.get("/")  # Replace with actual endpoint

# Save results to CSV after test completion
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

    results_file = "reports/test_results.csv"
    os.makedirs(os.path.dirname(results_file), exist_ok=True)

    df = pd.DataFrame(stats)
    df.to_csv(results_file, index=False)
    print(f"✅ Results saved to {results_file}")
