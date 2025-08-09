"""
Layout components for the Invoice OCR application
"""
import streamlit as st
import os
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

def get_environment_variable(key: str, default: str = "") -> str:
    """
    Get environment variable with fallback to Streamlit secrets
    
    Args:
        key: Environment variable key
        default: Default value if not found
    
    Returns:
        Environment variable value
    """
    # First try environment variables (GitHub Actions/deployment)
    value = os.environ.get(key)
    
    # If not found, try Streamlit secrets (local development)
    if not value:
        try:
            value = st.secrets.get(key, default)
        except (FileNotFoundError, KeyError):
            value = default
    
    return value

def render_header():
    """Render the main application header"""
    st.markdown("""
    <div class="main-header">
        <h1>📄 Invoice Data Extraction</h1>
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
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Configuration Section
        def render_api_settings():
            # Get API key from environment variables or secrets
            default_api_key = get_environment_variable("OPENROUTER_API_KEY")
            
            # Show different UI based on whether API key is pre-configured
            if default_api_key:
                st.success("✅ API Key loaded from environment")
                config['api_key'] = default_api_key
                
                # Option to override if needed
                with st.expander("🔑 Override API Key"):
                    override_key = st.text_input(
                        "Custom API Key", 
                        type="password", 
                        help="Leave empty to use environment variable"
                    )
                    if override_key:
                        config['api_key'] = override_key
            else:
                config['api_key'] = st.text_input(
                    "OpenRouter API Key", 
                    type="password", 
                    help="Enter your OpenRouter API key (or set OPENROUTER_API_KEY environment variable)",
                    placeholder="Required: Enter your OpenRouter API key"
                )
            
            # Get other settings from environment with fallbacks
            default_site_url = get_environment_variable("OPENROUTER_SITE_URL", "https://localhost:8501")
            default_site_name = get_environment_variable("OPENROUTER_SITE_NAME", "Invoice OCR Extractor")
            
            config['api_endpoint'] = st.text_input(
                "API Endpoint", 
                value=DEFAULT_API_ENDPOINT, 
                help="OpenRouter API endpoint"
            )
            
            # Show environment values or allow override
            with st.expander("🌐 Site Configuration"):
                config['site_url'] = st.text_input(
                    "Site URL", 
                    value=default_site_url, 
                    help="Your site URL for OpenRouter rankings"
                )
                config['site_name'] = st.text_input(
                    "Site Name", 
                    value=default_site_name, 
                    help="Your site name for OpenRouter rankings"
                )
        
        create_sidebar_section("API Settings", render_api_settings)
        
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
        
        # Environment Status Section
        def render_environment_status():
            st.markdown("**🌍 Environment Status**")
            
            # Check environment variables
            env_vars = {
                "OPENROUTER_API_KEY": "🔑 API Key",
                "OPENROUTER_SITE_URL": "🌐 Site URL", 
                "OPENROUTER_SITE_NAME": "📛 Site Name"
            }
            
            for env_var, display_name in env_vars.items():
                if os.environ.get(env_var):
                    st.success(f"✅ {display_name} (Environment)")
                elif get_environment_variable(env_var):
                    st.info(f"ℹ️ {display_name} (Secrets)")
                else:
                    if env_var == "OPENROUTER_API_KEY":
                        st.error(f"❌ {display_name} (Missing)")
                    else:
                        st.warning(f"⚠️ {display_name} (Default)")
            
            # API Status
            if config.get('api_key'):
                st.success("🚀 Ready to process")
            else:
                st.error("⛔ API Key required")
            
            # Show selected extraction fields
            selected_fields = [
                EXTRACTION_FIELDS[key]['label'] 
                for key, value in config.items() 
                if key in EXTRACTION_FIELDS and value
            ]
            
            if selected_fields:
                st.info(f"📋 Extracting: {', '.join(selected_fields)}")
        
        create_sidebar_section("Status", render_environment_status)
    
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
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("📷 PNG")
        with col2:
            st.write("🖼️ JPG/JPEG")
        with col3:
            st.write("📄 PDF (coming soon)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded_file

def render_results_section():
    """Render the results section with extracted data"""
    if not hasattr(st.session_state, 'extracted_data'):
        return
    
    data = st.session_state.extracted_data
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    st.markdown("### 📊 Extracted Invoice Data")
    
    # Basic Information Cards
    render_basic_info_cards(data)
    
    # Detailed Information Sections
    col1, col2 = st.columns(2)
    
    with col1:
        # Vendor Information
        if data.get('vendor'):
            display_vendor_info(data['vendor'])
        
        # Financial Summary
        display_financial_summary(data)
    
    with col2:
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
    col1, col2, col3, col4 = st.columns(4)
    
    # Invoice Number
    display_metric_card(
        "Invoice #", 
        data.get('invoice_number', 'N/A'), 
        col1
    )
    
    # Invoice Date
    display_metric_card(
        "Date", 
        data.get('invoice_date', 'N/A'), 
        col2
    )
    
    # Total Amount
    currency = data.get('currency', '')
    total = data.get('total_amount', 'N/A')
    total_display = f"{currency} {total}".strip() if total != 'N/A' else 'N/A'
    display_metric_card(
        "Total Amount", 
        total_display, 
        col3
    )
    
    # Due Date
    display_metric_card(
        "Due Date", 
        data.get('due_date', 'N/A'), 
        col4
    )

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

def render_environment_info():
    """Render environment information for debugging"""
    if st.checkbox("🔍 Show Environment Debug Info"):
        st.markdown("**Environment Variables:**")
        
        env_vars = ["OPENROUTER_API_KEY", "OPENROUTER_SITE_URL", "OPENROUTER_SITE_NAME"]
        for var in env_vars:
            value = os.environ.get(var)
            if value:
                # Mask API key for security
                if "API_KEY" in var:
                    masked_value = f"{value[:8]}..." if len(value) > 8 else "***"
                    st.code(f"{var}={masked_value}")
                else:
                    st.code(f"{var}={value}")
            else:
                st.code(f"{var}=Not Set")

def render_footer():
    """Render application footer"""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏢 Powered by**")
        st.write("Qwen 2.5 VL")
    
    with col2:
        st.markdown("**🛠️ Built with**")
        st.write("Streamlit + OpenRouter")
    
    with col3:
        st.markdown("**📊 Features**")
        st.write("OCR • Data Export • AI Extraction")
