import streamlit as st
import subprocess
import pandas as pd
import os
import utils  # Import export functions

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
            st.error("⚠️ Locust encountered an error while running.")
        else:
            st.success("✅ Test Completed! Download results below.")

# Provide download options
st.subheader("📂 Download Test Results")
export_format = st.selectbox("Choose format", ["CSV", "HTML", "PDF"])
if st.button("📥 Generate & Download"):
    file_path = utils.export_results(export_format)
    if file_path:
        with open(file_path, "rb") as f:
            st.download_button(label="📥 Click to Download", data=f, file_name=os.path.basename(file_path))
        st.success(f"✅ Results exported as {export_format}!")
    else:
        st.error("⚠️ No test results available. Please run a test first.")
