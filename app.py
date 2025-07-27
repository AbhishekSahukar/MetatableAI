import streamlit as st
import tempfile
from tools.utils import format_parameters_table, export_csv, export_json
from graph_builder import build_metatable_graph  


st.set_page_config(page_title="MetaTableAI (LangGraph)", layout="centered")
st.title("📊 MetaTableAI (LangGraph-powered)")

uploaded_file = st.file_uploader("📁 Upload a technical PDF with tables or parameters:", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    st.success("✅ File uploaded successfully.")

    # Run LangGraph pipeline
    with st.spinner("🧠 Running LangGraph agent pipeline..."):
        graph = build_metatable_graph ()
        result = graph.invoke({"pdf_path": pdf_path})

    extracted_params = result.get("extracted_params", [])
    extracted_text = result.get("extracted_text", "")  # ✅ FIXED key

    if not extracted_params:
        st.warning("⚠️ No structured parameter-values found. Try another PDF.")
    else:
        df = format_parameters_table(extracted_params)
        st.success(f"✅ Extracted {len(df)} parameter-value pairs.")
        st.dataframe(df, use_container_width=True)

        st.download_button("📥 Download as CSV", export_csv(df), file_name="parameters.csv")
        st.download_button("📥 Download as JSON", export_json(df), file_name="parameters.json")

    with st.expander("📄 Preview Extracted Text"):
        st.text_area("Raw Text", extracted_text, height=300)

    with st.expander("🧠 Debug Result"):
        st.json(result)
