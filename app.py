import streamlit as st
import subprocess
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
from utils import export_results

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
    with open("urls.txt", "w") as f:
        f.write(urls)

    # Run Locust in headless mode
    command = f"locust -f locust_test.py --headless -u {users} -r {spawn_rate} --run-time {duration}s"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Save results
    with open("reports/test_results.json", "w") as f:
        f.write(process.stdout)

    st.success("Test Completed! Check the reports.")

    # Load results
    with open("reports/test_results.json") as f:
        results = json.load(f)
    
    # Display results
    st.subheader("Test Summary")
    st.write(results)

    # Generate chart
    st.subheader("Response Time Distribution")
    fig, ax = plt.subplots()
    ax.hist([r['response_time'] for r in results], bins=10)
    st.pyplot(fig)

    # Export options
    export_format = st.selectbox("Export Results As", ["CSV", "JSON", "PDF"])
    if st.button("Export"):
        export_results(results, export_format)
        st.success(f"Results exported as {export_format}!")
