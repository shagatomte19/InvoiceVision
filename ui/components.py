"""
Reusable UI components for the Invoice OCR application
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from utils.data_parser import format_currency

def display_metric_card(title: str, value: str, col=None):
    """
    Display a metric card with title and value
    
    Args:
        title: Card title
        value: Card value
        col: Streamlit column (optional)
    """
    container = col if col else st
    container.markdown(f"""
    <div class="metric-card">
        <h4>{title}</h4>
        <p>{value}</p>
    </div>
    """, unsafe_allow_html=True)

def display_info_section(title: str, content: str, section_type: str = "info"):
    """
    Display an information section with styling
    
    Args:
        title: Section title
        content: Section content
        section_type: Type of section (info, warning, error, success)
    """
    class_name = f"{section_type}-container"
    st.markdown(f"""
    <div class="{class_name}">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def display_vendor_info(vendor_data: Dict[str, str]):
    """
    Display vendor information in a styled container
    
    Args:
        vendor_data: Dictionary containing vendor information
    """
    if not vendor_data:
        return
    
    st.markdown("#### 🏢 Vendor Information")
    st.markdown('<div class="vendor-info">', unsafe_allow_html=True)
    
    # Remove nested columns - display in a clean vertical layout
    st.write(f"**Name:** {vendor_data.get('name', 'N/A')}")
    st.write(f"**Phone:** {vendor_data.get('phone', 'N/A')}")
    st.write(f"**Email:** {vendor_data.get('email', 'N/A')}")
    st.write(f"**Address:** {vendor_data.get('address', 'N/A')}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_billing_info(billing_data: Dict[str, str]):
    """
    Display billing information
    
    Args:
        billing_data: Dictionary containing billing information
    """
    if not billing_data:
        return
    
    st.markdown("#### 📧 Billing Information")
    st.markdown('<div class="info-section">', unsafe_allow_html=True)
    st.write(f"**Name:** {billing_data.get('name', 'N/A')}")
    st.write(f"**Address:** {billing_data.get('address', 'N/A')}")
    st.markdown('</div>', unsafe_allow_html=True)

def display_line_items(line_items: List[Dict[str, str]], currency: str = ""):
    """
    Display line items in a formatted table
    
    Args:
        line_items: List of line item dictionaries
        currency: Currency symbol/code
    """
    if not line_items or len(line_items) == 0:
        return
    
    st.markdown("#### 📋 Line Items")
    
    # Format line items for display
    formatted_items = []
    for item in line_items:
        formatted_item = {
            'Description': item.get('description', 'N/A'),
            'Quantity': item.get('quantity', 'N/A'),
            'Unit Price': format_currency(item.get('unit_price', ''), currency),
            'Total': format_currency(item.get('total', ''), currency)
        }
        formatted_items.append(formatted_item)
    
    # Create DataFrame and display
    df = pd.DataFrame(formatted_items)
    st.dataframe(df, use_container_width=True, hide_index=True)

def display_financial_summary(data: Dict[str, Any]):
    """
    Display financial summary information
    
    Args:
        data: Invoice data containing financial information
    """
    currency = data.get('currency', '')
    
    st.markdown("#### 💰 Financial Summary")
    st.markdown('<div class="financial-summary">', unsafe_allow_html=True)
    
    # Remove nested columns - display in a clean vertical layout
    st.write(f"**Subtotal:** {format_currency(data.get('subtotal', ''), currency)}")
    st.write(f"**Tax Rate:** {data.get('tax_rate', 'N/A')}")
    st.write(f"**Tax Amount:** {format_currency(data.get('tax_amount', ''), currency)}")
    st.write(f"**Total Amount:** {format_currency(data.get('total_amount', ''), currency)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_extraction_stats(data: Dict[str, Any]):
    """
    Display extraction statistics
    
    Args:
        data: Invoice data
    """
    # Count extracted fields
    total_fields = 0
    extracted_fields = 0
    
    # Basic fields
    basic_fields = ['invoice_number', 'invoice_date', 'total_amount']
    for field in basic_fields:
        total_fields += 1
        if data.get(field):
            extracted_fields += 1
    
    # Vendor fields
    if data.get('vendor'):
        vendor_fields = ['name', 'address', 'phone', 'email']
        for field in vendor_fields:
            total_fields += 1
            if data['vendor'].get(field):
                extracted_fields += 1
    
    # Line items
    if data.get('line_items'):
        total_fields += 1
        if len(data['line_items']) > 0:
            extracted_fields += 1
    
    # Calculate extraction rate
    extraction_rate = (extracted_fields / total_fields * 100) if total_fields > 0 else 0
    
    st.markdown("#### 📊 Extraction Statistics")
    
    # Use metric cards in a single row (this should work as it's at the top level)
    col1, col2, col3 = st.columns(3)
    
    display_metric_card("Fields Extracted", f"{extracted_fields}/{total_fields}", col1)
    display_metric_card("Success Rate", f"{extraction_rate:.1f}%", col2)
    display_metric_card("Line Items", str(len(data.get('line_items', []))), col3)

def create_download_section(data: Dict[str, Any]):
    """
    Create download section with export options
    
    Args:
        data: Invoice data to export
    """
    st.markdown("### 💾 Export Options")
    
    # Check if this function is called within existing columns
    # If so, display vertically instead of creating new columns
    st.markdown("**📄 JSON Export** - Complete invoice data with all extracted fields")
    st.markdown("**📊 CSV Export** - Line items in spreadsheet format")  
    st.markdown("**📋 Summary** - Key metrics and totals")

def display_processing_status(status: str, message: str = ""):
    """
    Display processing status with appropriate styling
    
    Args:
        status: Status type (processing, success, error, warning)
        message: Status message
    """
    if status == "processing":
        st.info(f"🔄 {message}")
    elif status == "success":
        st.success(f"✅ {message}")
    elif status == "error":
        st.error(f"❌ {message}")
    elif status == "warning":
        st.warning(f"⚠️ {message}")

def create_sidebar_section(title: str, content_func):
    """
    Create a styled sidebar section
    
    Args:
        title: Section title
        content_func: Function to render section content
    """
    st.markdown(f'<div class="sidebar-section">', unsafe_allow_html=True)
    st.subheader(title)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)
