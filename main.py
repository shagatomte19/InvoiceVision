"""
Main Streamlit application for Invoice OCR Extraction
"""
import streamlit as st
from ui.layout import render_header, render_sidebar, render_upload_section, render_results_section
from ui.styles import load_custom_styles
from config.settings import PAGE_CONFIG
from utils.export_utils import handle_export_options

def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(**PAGE_CONFIG)
    
    # Load custom styles
    load_custom_styles()
    
    # Initialize session state
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    
    # Render header
    render_header()
    
    # Render sidebar and get configuration
    config = render_sidebar()
    
    # Main content area - remove columns to avoid nesting issues
    # Upload section
    st.markdown("### 📤 Upload Invoice")
    uploaded_file = render_upload_section()
    
    if uploaded_file is not None:
        from utils.image_processor import process_uploaded_file
        process_uploaded_file(uploaded_file, config)
    
    # Results section - display below upload section
    if st.session_state.processing_complete:
        st.markdown("---")  # Separator between sections
        st.markdown("### 📊 Extraction Results")
        render_results_section()
        handle_export_options()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>📄 Invoice OCR Extractor powered by Qwen 2.5 VL via OpenRouter | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
