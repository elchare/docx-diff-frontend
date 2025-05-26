import streamlit as st
import requests
import os

st.set_page_config(page_title="DOCX Diff Tool", layout="centered")

st.title("📄 DOCX Tracked Changes Extractor")
st.markdown("Upload one or more `.docx` files and extract tracked changes involving specific keywords (e.g., `MUST`, `SHOULD`, `MAY`).")

api_url = st.text_input("🔗 API Endpoint (FastAPI backend)", value="https://docx-diff-api.onrender.com/process")
keywords = st.text_input("🧩 Keywords to Filter (comma-separated)", value="MUST,SHOULD,MAY")
case_sensitive = st.checkbox("Case sensitive match", value=True)
whole_word = st.checkbox("Match whole words only", value=True)

# Safe sample file download
st.markdown("### 📥 Try with a Sample DOCX File")
sample_path = "examples/sample_docxdiff.docx"
if os.path.exists(sample_path):
    with open(sample_path, "rb") as sample_file:
        st.download_button(
            label="📄 Download Sample DOCX File",
            data=sample_file,
            file_name="sample_docxdiff.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
else:
    st.info("⚠️ Sample file not found in `examples/`")

st.markdown("---")

uploaded_files = st.file_uploader("📁 Upload .docx file(s)", type=["docx"], accept_multiple_files=True)

if st.button("🚀 Process Files") and uploaded_files:
    for file in uploaded_files:
        with st.spinner(f"Processing `{file.name}`..."):
            try:
                headers = {}
                if "API_KEY" in st.secrets:
                    headers["x-api-key"] = st.secrets["API_KEY"]

                response = requests.post(
                    api_url,
                    headers=headers,
                    files={"file": (file.name, file.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
                    data={
                        "keywords": keywords,
                        "case_sensitive": str(case_sensitive).lower(),
                        "whole_word": str(whole_word).lower()
                    },
                )

                if response.status_code == 200:
                    st.success(f"✅ Processed `{file.name}`")
                    st.download_button(
                        label=f"⬇️ Download Excel for {file.name}",
                        data=response.content,
                        file_name=f"{file.name}_diff.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error(f"❌ Failed to process `{file.name}`. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error while processing `{file.name}`: {e}")
