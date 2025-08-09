"""
Data parsing utilities for invoice extraction results
"""
import json
import re
import streamlit as st
from typing import Dict, Any, Optional
from models.invoice_model import InvoiceData

def parse_extraction_result(api_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Parse the API response and extract JSON data
    
    Args:
        api_response: Raw API response
        
    Returns:
        Parsed invoice data or None if error
    """
    try:
        content = api_response['choices'][0]['message']['content']
        
        # Try to find JSON in the response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            parsed_data = json.loads(json_str)
            
            # Validate and clean the data
            return validate_invoice_data(parsed_data)
        else:
            st.warning("No JSON structure found in the response")
            return {"raw_response": content}
            
    except (KeyError, json.JSONDecodeError) as e:
        st.error(f"Error parsing response: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error in parsing: {str(e)}")
        return None

def validate_invoice_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean invoice data
    
    Args:
        data: Raw parsed data
        
    Returns:
        Cleaned and validated data
    """
    # Create InvoiceData instance for validation
    invoice = InvoiceData()
    
    try:
        # Basic fields
        invoice.invoice_number = clean_string(data.get('invoice_number', ''))
        invoice.invoice_date = clean_string(data.get('invoice_date', ''))
        invoice.due_date = clean_string(data.get('due_date', ''))
        invoice.currency = clean_string(data.get('currency', ''))
        
        # Financial fields
        invoice.subtotal = clean_currency(data.get('subtotal', ''))
        invoice.tax_amount = clean_currency(data.get('tax_amount', ''))
        invoice.tax_rate = clean_string(data.get('tax_rate', ''))
        invoice.total_amount = clean_currency(data.get('total_amount', ''))
        
        # Vendor information
        vendor_data = data.get('vendor', {})
        if vendor_data:
            invoice.vendor = {
                'name': clean_string(vendor_data.get('name', '')),
                'address': clean_string(vendor_data.get('address', '')),
                'phone': clean_string(vendor_data.get('phone', '')),
                'email': clean_string(vendor_data.get('email', ''))
            }
        
        # Billing information
        billing_data = data.get('billing_to', {})
        if billing_data:
            invoice.billing_to = {
                'name': clean_string(billing_data.get('name', '')),
                'address': clean_string(billing_data.get('address', ''))
            }
        
        # Line items
        line_items = data.get('line_items', [])
        if line_items:
            invoice.line_items = []
            for item in line_items:
                if isinstance(item, dict):
                    cleaned_item = {
                        'description': clean_string(item.get('description', '')),
                        'quantity': clean_string(item.get('quantity', '')),
                        'unit_price': clean_currency(item.get('unit_price', '')),
                        'total': clean_currency(item.get('total', ''))
                    }
                    invoice.line_items.append(cleaned_item)
        
        return invoice.to_dict()
        
    except Exception as e:
        st.warning(f"Data validation warning: {str(e)}")
        return data

def clean_string(value: Any) -> str:
    """
    Clean and normalize string values
    
    Args:
        value: Input value
        
    Returns:
        Cleaned string
    """
    if value is None:
        return ''
    
    # Convert to string and strip whitespace
    cleaned = str(value).strip()
    
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    return cleaned

def clean_currency(value: Any) -> str:
    """
    Clean currency values
    
    Args:
        value: Input currency value
        
    Returns:
        Cleaned currency string
    """
    if value is None:
        return ''
    
    # Convert to string and remove extra whitespace
    cleaned = str(value).strip()
    
    # Remove currency symbols and extra characters, keep numbers and decimal points
    cleaned = re.sub(r'[^\d.,]', '', cleaned)
    
    # Normalize decimal separators
    if ',' in cleaned and '.' in cleaned:
        # If both comma and dot, assume comma is thousands separator
        cleaned = cleaned.replace(',', '')
    elif ',' in cleaned and '.' not in cleaned:
        # If only comma, it might be decimal separator (European format)
        if len(cleaned.split(',')[-1]) <= 2:
            cleaned = cleaned.replace(',', '.')
        else:
            cleaned = cleaned.replace(',', '')
    
    return cleaned

def format_currency(amount: str, currency: str = '') -> str:
    """
    Format currency for display
    
    Args:
        amount: Amount string
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    if not amount:
        return 'N/A'
    
    try:
        # Try to format as float
        float_amount = float(amount)
        formatted = f"{float_amount:,.2f}"
        return f"{currency} {formatted}".strip()
    except ValueError:
        return f"{currency} {amount}".strip()