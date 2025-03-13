import streamlit as st
import subprocess
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
from utils import export_results

# Ensure necessary directories exist
os.makedirs("reports", exist_ok=True)

# Streamlit App UI
st.title("OverloadX-2.0 - Load Testing Tool")

# User input for URLs
st.subheader("Enter URLs for Testing")
urls = st.text_area("Enter multiple URLs (one per line)", height=150)

# Test type selection
test_type = st.selectbox("Select Test Type", ["Load", "Stress", "Spike"])

# Test parameters
users = st.slider("Number of Users", 1, 100, 10)
spawn_rate = st.slider("Spawn Rate", 1, 20, 2)
duration = st.slider("Test Duration (seconds)", 10, 300, 30)

# Start test button
if st.button("Start Test"):
    if not urls.strip():
        st.error("Please enter at least one URL.")
    else:
        # Save URLs to a file
        with open("urls.txt", "w") as f:
            f.write(urls)

        # Run Locust in headless mode
        command = f"locust -f locust_test.py --headless -u {users} -r {spawn_rate} --run-time {duration}s"
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check for errors
        if process.returncode != 0:
            st.error("An error occurred while running Locust.")
            st.text(process.stderr)
        else:
            st.success("Test Completed! Check the reports.")

# Load results if available
st.subheader("Test Results")
results_file = "reports/test_results.json"

if os.path.exists(results_file) and os.path.getsize(results_file) > 0:
    with open(results_file) as f:
        results = json.load(f)

    # Debug: Print JSON structure
    st.subheader("Raw Test Data")
    st.write(results)  # Print raw JSON output to inspect structure

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Check if 'avg_response_time' exists
    if "avg_response_time" not in df.columns:
        st.error("The key 'avg_response_time' is missing in test results. Check the raw test data.")
    else:
        # Display key metrics
        st.write(df)

        # Generate chart for response times
        st.subheader("Response Time Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["avg_response_time"], bins=10, edgecolor="black")
        ax.set_xlabel("Response Time (ms)")
        ax.set_ylabel("Frequency")
        ax.set_title("Response Time Distribution")
        st.pyplot(fig)

    # Export options
    export_format = st.selectbox("Export Results As", ["CSV", "JSON", "PDF"])
    if st.button("Export"):
        export_results(results, export_format)
        st.success(f"Results exported as {export_format}!")
else:
    st.warning("No valid test results found. Please run the test again.")
