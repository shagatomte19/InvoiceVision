"""
Export utilities for invoice data
"""
import json
import pandas as pd
import streamlit as st
from datetime import datetime
from typing import Dict, Any
from config.settings import JSON_INDENT

def handle_export_options() -> None:
    """Handle export functionality in the UI"""
    if not hasattr(st.session_state, 'extracted_data'):
        return
    
    st.markdown("### 💾 Export Data")
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        if st.button("📄 Export as JSON"):
            json_data = export_to_json(st.session_state.extracted_data)
            if json_data:
                st.download_button(
                    "Download JSON",
                    json_data,
                    file_name=generate_filename('json'),
                    mime="application/json"
                )
    
    with export_col2:
        if st.button("📊 Export as CSV"):
            csv_data = export_to_csv(st.session_state.extracted_data)
            if csv_data:
                st.download_button(
                    "Download CSV",
                    csv_data,
                    file_name=generate_filename('csv'),
                    mime="text/csv"
                )

def export_to_json(data: Dict[str, Any]) -> str:
    """
    Export invoice data to JSON format
    
    Args:
        data: Invoice data dictionary
        
    Returns:
        JSON string
    """
    try:
        return json.dumps(data, indent=JSON_INDENT, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error exporting to JSON: {str(e)}")
        return None

def export_to_csv(data: Dict[str, Any]) -> str:
    """
    Export invoice line items to CSV format
    
    Args:
        data: Invoice data dictionary
        
    Returns:
        CSV string or None if no line items
    """
    try:
        line_items = data.get('line_items', [])
        if not line_items:
            st.warning("No line items found to export to CSV")
            return None
        
        # Create DataFrame from line items
        df = pd.DataFrame(line_items)
        
        # Add invoice metadata as additional columns
        metadata_cols = {
            'invoice_number': data.get('invoice_number', ''),
            'invoice_date': data.get('invoice_date', ''),
            'vendor_name': data.get('vendor', {}).get('name', ''),
            'total_amount': data.get('total_amount', ''),
            'currency': data.get('currency', '')
        }
        
        for col, value in metadata_cols.items():
            df[col] = value
        
        return df.to_csv(index=False)
        
    except Exception as e:
        st.error(f"Error exporting to CSV: {str(e)}")
        return None

def generate_filename(extension: str) -> str:
    """
    Generate filename with timestamp
    
    Args:
        extension: File extension (json, csv)
        
    Returns:
        Filename string
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if extension == 'json':
        return f"invoice_data_{timestamp}.json"
    elif extension == 'csv':
        return f"invoice_items_{timestamp}.csv"
    else:
        return f"invoice_export_{timestamp}.{extension}"

def prepare_export_data(data: Dict[str, Any], export_format: str) -> Dict[str, Any]:
    """
    Prepare data for export by cleaning and formatting
    
    Args:
        data: Raw invoice data
        export_format: Target format (json, csv)
        
    Returns:
        Prepared data dictionary
    """
    if export_format == 'json':
        # For JSON, include all data
        return data
    elif export_format == 'csv':
        # For CSV, focus on line items with metadata
        line_items = data.get('line_items', [])
        if not line_items:
            return {'error': 'No line items available for CSV export'}
        
        # Add metadata to each line item
        metadata = {
            'invoice_number': data.get('invoice_number', ''),
            'invoice_date': data.get('invoice_date', ''),
            'vendor_name': data.get('vendor', {}).get('name', ''),
            'total_amount': data.get('total_amount', ''),
            'currency': data.get('currency', '')
        }
        
        enhanced_items = []
        for item in line_items:
            enhanced_item = {**item, **metadata}
            enhanced_items.append(enhanced_item)
        
        return {'line_items': enhanced_items}
    
    return data