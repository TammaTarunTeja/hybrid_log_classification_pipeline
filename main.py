import streamlit as st
import requests
import pandas as pd
import io

st.set_page_config(page_title="Log Classifier", layout="centered")

st.title("📊 Log Message Classifier")
st.info("Upload a CSV file with 'log_message' and 'source' columns to begin.")

# 1. File Uploader (No preview shown)
uploaded_file = st.file_uploader("Choose a CSV file", type="csv", label_visibility="collapsed")

if uploaded_file is not None:
    # 2. Classification Button
    if st.button("🚀 Run Classification", use_container_width=True):
        with st.spinner("Processing logs on the server..."):
            try:
                # Prepare the file for the FastAPI endpoint
                uploaded_file.seek(0)
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                
                # Request to fixed localhost address
                response = requests.post("http://127.0.0.1:8000/classify", files=files)

                if response.status_code == 200:
                    # Convert response content to DataFrame
                    result_df = pd.read_csv(io.BytesIO(response.content))
                    
                    st.success("✅ Success! Your classified logs are ready.")

                    # --- DOWNLOAD SECTION ---
                    st.write("### Download Results")
                    col1, col2 = st.columns(2)

                    with col1:
                        # CSV download logic
                        csv_data = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download as CSV",
                            data=csv_data,
                            file_name="classified_logs.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

                    with col2:
                        # Excel download logic (Uses xlsxwriter)
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                            result_df.to_excel(writer, index=False, sheet_name='Logs')
                        
                        st.download_button(
                            label="📄 Download as Excel",
                            data=buffer.getvalue(),
                            file_name="classified_logs.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                else:
                    st.error(f"❌ Server Error: {response.status_code}. Check column names.")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Failed. Is 'server.py' running at http://127.0.0.1:8000?")