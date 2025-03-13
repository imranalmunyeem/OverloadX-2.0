import streamlit as st
import subprocess
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import utils  # Import utils properly

# Ensure necessary directories exist
os.makedirs("reports", exist_ok=True)

# Streamlit App UI
st.title("🚀 OverloadX-2.0 - Load Testing Tool")

# User input for URLs
st.subheader("🔗 Enter URLs for Testing")
urls = st.text_area("Enter multiple URLs (one per line)", height=150)

# Test type selection
test_type = st.selectbox("🛠️ Select Test Type", ["Load", "Stress", "Spike"])

# Test parameters
users = st.slider("👥 Number of Users", 1, 100, 10)
spawn_rate = st.slider("📈 Spawn Rate (Users per Second)", 1, 20, 2)
duration = st.slider("⏳ Test Duration (Seconds)", 10, 300, 30)

# Start test button
if st.button("🚀 Start Load Test"):
    if not urls.strip():
        st.error("⚠️ Please enter at least one URL.")
    else:
        # Save URLs to a file
        with open("urls.txt", "w") as f:
            f.write(urls)

        # Run Locust in headless mode
        command = f"locust -f locust_test.py --headless -u {users} -r {spawn_rate} --run-time {duration}s"
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check for errors
        if process.returncode != 0:
            st.error("⚠️ An error occurred while running Locust.")
            st.text(process.stderr)
        else:
            st.success("✅ Test Completed! Check the reports below.")

# Load and display test results
st.subheader("📊 Test Results")
results_file = "reports/test_results.json"

if os.path.exists(results_file) and os.path.getsize(results_file) > 0:
    try:
        with open(results_file) as f:
            results = json.load(f)

        if not results or results[0]["num_requests"] == 0:
            st.warning("⚠️ No requests were made during the test. Please check your URLs and try again.")
        else:
            # Convert to DataFrame
            df = pd.DataFrame(results)

            # Ensure required keys exist
            expected_keys = ["name", "method", "num_requests", "num_failures", "avg_response_time"]
            missing_keys = [key for key in expected_keys if key not in df.columns]

            if missing_keys:
                st.warning(f"⚠️ Missing test data: {', '.join(missing_keys)}. Displaying available results.")

            # Display summary metrics
            st.write("### 📌 Summary of Test Metrics")
            metrics = {
                "Total Requests": df["num_requests"].sum(),
                "Total Failures": df["num_failures"].sum(),
                "Average Response Time (ms)": round(df["avg_response_time"].mean(), 2),
                "Min Response Time (ms)": df["min_response_time"].min(),
                "Max Response Time (ms)": df["max_response_time"].max(),
                "Requests Per Second": round(df["requests_per_second"].mean(), 2),
            }
            st.table(pd.DataFrame(metrics, index=["Values"]))

            # Display detailed breakdown
            st.write("### 📌 Detailed Endpoint Performance")
            df_display = df[["name", "method", "num_requests", "num_failures", "avg_response_time"]]
            df_display = df_display.rename(columns={
                "name": "Endpoint",
                "method": "Method",
                "num_requests": "Requests",
                "num_failures": "Failures",
                "avg_response_time": "Avg Response Time (ms)"
            })
            st.table(df_display)

            # Generate response time chart
            st.subheader("📈 Response Time Distribution")
            fig, ax = plt.subplots()
            ax.hist(df["avg_response_time"], bins=10, edgecolor="black")
            ax.set_xlabel("Response Time (ms)")
            ax.set_ylabel("Frequency")
            ax.set_title("Response Time Distribution")
            st.pyplot(fig)

            # Export options
            st.subheader("📂 Export Results")
            export_format = st.selectbox("Choose format", ["CSV", "JSON", "PDF"])
            if st.button("📥 Export"):
                utils.export_results(results, export_format)
                st.success(f"✅ Results exported as {export_format}!")

    except json.JSONDecodeError:
        st.error("⚠️ Test results file is corrupted or empty. Run a test first.")
else:
    st.warning("⚠️ No test results found. Run a test first.")
