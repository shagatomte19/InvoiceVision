"""
Configuration settings for the Invoice OCR application
"""

# Streamlit page configuration
PAGE_CONFIG = {
    "page_title": "InvoiceVision",
    "page_icon": "📄",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# API configuration
DEFAULT_API_ENDPOINT = "https://openrouter.ai/api/v1"
SUPPORTED_MODELS = [
    "qwen/qwen2.5-vl-72b-instruct:free",
    "qwen/qwen2.5-vl-7b-instruct",
    "qwen/qwen2.5-vl-3b-instruct"
]

# OpenRouter specific settings
DEFAULT_SITE_URL = "https://localhost:8501"  # Default for local Streamlit
DEFAULT_SITE_NAME = "InvoiceVision"

# File upload settings
SUPPORTED_IMAGE_TYPES = ['png', 'jpg', 'jpeg']
SUPPORTED_FILE_TYPES = ['png', 'jpg', 'jpeg', 'pdf']

# Model parameters
DEFAULT_TEMPERATURE = 0.4
DEFAULT_MAX_TOKENS = 2000
MIN_TEMPERATURE = 0.0
MAX_TEMPERATURE = 1.0
MIN_TOKENS = 500
MAX_TOKENS = 4000

# Extraction options
EXTRACTION_FIELDS = {
    'extract_vendor': {
        'label': 'Extract Vendor Info',
        'default': True,
        'description': 'vendor/supplier information'
    },
    'extract_dates': {
        'label': 'Extract Dates',
        'default': True,
        'description': 'invoice date and due date'
    },
    'extract_totals': {
        'label': 'Extract Totals',
        'default': True,
        'description': 'subtotal, tax, and total amounts'
    },
    'extract_items': {
        'label': 'Extract Line Items',
        'default': True,
        'description': 'line items with descriptions, quantities, and prices'
    }
}

# Export settings
EXPORT_FORMATS = ['json', 'csv']

JSON_INDENT = 2
