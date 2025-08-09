"""
Layout components for the Invoice OCR application
"""
import streamlit as st
from typing import Dict, Any
from config.settings import (
    SUPPORTED_FILE_TYPES, 
    SUPPORTED_MODELS, 
    DEFAULT_TEMPERATURE, 
    DEFAULT_MAX_TOKENS,
    MIN_TEMPERATURE, 
    MAX_TEMPERATURE, 
    MIN_TOKENS, 
    MAX_TOKENS,
    DEFAULT_API_ENDPOINT,
    EXTRACTION_FIELDS
)
from ui.components import (
    display_metric_card, 
    display_vendor_info, 
    display_billing_info,
    display_line_items, 
    display_financial_summary, 
    display_extraction_stats,
    create_sidebar_section
)

def render_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>📄 InvoiceVision</h1>
        <p>Upload your invoice images and extract structured data using Qwen 2.5 VL via OpenRouter</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar() -> Dict[str, Any]:
    """
    Render sidebar with configuration options
    
    Returns:
        Dictionary containing all configuration values
    """
    config = {}
    
    # Set API configuration from secrets or defaults
    try:
        config['api_key'] = st.secrets.get("OPENROUTER_API_KEY", "")
        config['site_url'] = st.secrets.get("OPENROUTER_SITE_URL", "https://localhost:8501")
        config['site_name'] = st.secrets.get("OPENROUTER_SITE_NAME", "Invoice OCR Extractor")
    except:
        config['api_key'] = ""
        config['site_url'] = "https://localhost:8501"
        config['site_name'] = "Invoice OCR Extractor"
    
    config['api_endpoint'] = DEFAULT_API_ENDPOINT
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Model Configuration Section
        def render_model_settings():
            config['model_name'] = st.selectbox(
                "Qwen Model", 
                SUPPORTED_MODELS, 
                index=0,
                help="Select the Qwen 2.5 VL model to use"
            )
            config['temperature'] = st.slider(
                "Temperature", 
                MIN_TEMPERATURE, 
                MAX_TEMPERATURE, 
                DEFAULT_TEMPERATURE, 
                help="Controls randomness in responses"
            )
            config['max_tokens'] = st.slider(
                "Max Tokens", 
                MIN_TOKENS, 
                MAX_TOKENS, 
                DEFAULT_MAX_TOKENS, 
                help="Maximum response length"
            )
        
        create_sidebar_section("Model Settings", render_model_settings)
        
        # Extraction Options Section
        def render_extraction_options():
            for field_key, field_config in EXTRACTION_FIELDS.items():
                config[field_key] = st.checkbox(
                    field_config['label'], 
                    value=field_config['default'],
                    help=f"Extract {field_config['description']}"
                )
        
        create_sidebar_section("Extraction Options", render_extraction_options)
        
        # Status Section
        def render_status():
            if config.get('api_key'):
                st.success("✅ API configured")
            else:
                st.warning("⚠️ API key not configured in secrets")
            
            # Show selected extraction fields
            selected_fields = [
                EXTRACTION_FIELDS[key]['label'] 
                for key, value in config.items() 
                if key in EXTRACTION_FIELDS and value
            ]
            
            if selected_fields:
                st.info(f"📋 Extracting: {', '.join(selected_fields)}")
        
        create_sidebar_section("Status", render_status)
    
    return config

def render_upload_section():
    """
    Render file upload section
    
    Returns:
        Uploaded file object or None
    """
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📤 Upload Invoice")
    
    uploaded_file = st.file_uploader(
        "Choose an invoice image...",
        type=SUPPORTED_FILE_TYPES,
        help=f"Upload {', '.join(SUPPORTED_FILE_TYPES).upper()} files"
    )
    
    if uploaded_file is None:
        st.info("👆 Please upload an invoice image to get started")
        
        # Show supported formats
        st.markdown("**Supported formats:**")
        st.markdown("📷 PNG • 🖼️ JPG/JPEG • 📄 PDF (coming soon)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded_file

def render_results_section():
    """Render the results section with extracted data"""
    if not hasattr(st.session_state, 'extracted_data'):
        return
    
    data = st.session_state.extracted_data
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Extracted Invoice Data")
    
    # Basic Information Cards - remove columns to avoid nesting
    render_basic_info_cards(data)
    
    # Detailed Information Sections - remove columns to avoid nesting
    # Vendor Information
    if data.get('vendor'):
        display_vendor_info(data['vendor'])
    
    # Financial Summary
    display_financial_summary(data)
    
    # Billing Information
    if data.get('billing_to'):
        display_billing_info(data['billing_to'])
    
    # Extraction Statistics
    display_extraction_stats(data)
    
    # Line Items (full width)
    if data.get('line_items'):
        display_line_items(data['line_items'], data.get('currency', ''))
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_basic_info_cards(data: Dict[str, Any]):
    """
    Render basic information as metric cards
    
    Args:
        data: Invoice data dictionary
    """
    st.markdown("#### 📋 Basic Information")
    
    # Display metrics vertically to avoid column nesting
    invoice_num = data.get('invoice_number', 'N/A')
    st.markdown(f"**Invoice #:** {invoice_num}")
    
    invoice_date = data.get('invoice_date', 'N/A')
    st.markdown(f"**Date:** {invoice_date}")
    
    currency = data.get('currency', '')
    total = data.get('total_amount', 'N/A')
    total_display = f"{currency} {total}".strip() if total != 'N/A' else 'N/A'
    st.markdown(f"**Total Amount:** {total_display}")
    
    due_date = data.get('due_date', 'N/A')
    st.markdown(f"**Due Date:** {due_date}")

def render_error_state(error_message: str):
    """
    Render error state
    
    Args:
        error_message: Error message to display
    """
    st.markdown(f"""
    <div class="error-container">
        <h4>❌ Processing Error</h4>
        <p>{error_message}</p>
    </div>
    """, unsafe_allow_html=True)

def render_loading_state(message: str = "Processing invoice..."):
    """
    Render loading state
    
    Args:
        message: Loading message
    """
    with st.spinner(message):
        st.info("🤖 AI is analyzing your invoice. This may take a few moments...")

def render_empty_state():
    """Render empty state when no data is available"""
    st.markdown("""
    <div class="info-section">
        <h4>📋 Ready to Extract</h4>
        <p>Upload an invoice image and click "Extract Data" to see the results here.</p>
    </div>
    """, unsafe_allow_html=True)

def render_help_section():
    """Render help and tips section"""
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        **For optimal extraction results:**
        
        1. **Image Quality**: Use high-resolution, clear images
        2. **Lighting**: Ensure good lighting with minimal shadows
        3. **Orientation**: Upload images in correct orientation
        4. **Format**: PNG and JPG work best
        5. **Content**: Ensure all text is clearly visible
        
        **Supported Invoice Types:**
        - Standard business invoices
        - Receipts with itemized lists
        - Purchase orders
        - Service bills
        """)

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("**🏢 Powered by** Qwen 2.5 VL • **🛠️ Built with** Streamlit + OpenRouter • **📊 Features** OCR • Data Export • AI Extraction")

