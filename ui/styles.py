"""
CSS styles for the Invoice OCR application
"""
import streamlit as st

def load_custom_styles():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .upload-section {
            background: #f8f9fa;
            padding: 2rem;
            border-radius: 10px;
            border: 2px dashed #dee2e6;
            margin-bottom: 2rem;
        }
        
        .results-container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #28a745;
        }
        
        .error-container {
            background: #f8d7da;
            color: #721c24;
            padding: 1rem;
            border-radius: 5px;
            border: 1px solid #f5c6cb;
            margin: 1rem 0;
        }
        
        .success-container {
            background: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            border: 1px solid #c3e6cb;
            margin: 1rem 0;
        }
        
        .warning-container {
            background: #fff3cd;
            color: #856404;
            padding: 1rem;
            border-radius: 5px;
            border: 1px solid #ffeaa7;
            margin: 1rem 0;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .metric-card h4 {
            margin: 0 0 0.5rem 0;
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        .metric-card p {
            margin: 0;
            font-size: 1.2rem;
            font-weight: bold;
        }
        
        .info-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #17a2b8;
            margin: 1rem 0;
        }
        
        .vendor-info {
            background: #e3f2fd;
            padding: 1rem;
            border-radius: 8px;
            border-left: 3px solid #2196f3;
        }
        
        .financial-summary {
            background: #f3e5f5;
            padding: 1rem;
            border-radius: 8px;
            border-left: 3px solid #9c27b0;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        .sidebar-section {
            padding: 1rem 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .sidebar-section:last-child {
            border-bottom: none;
        }
        
        /* Custom styling for dataframes */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Custom styling for file uploader */
        .stFileUploader > div > div {
            border-radius: 10px;
        }
        
        /* Custom styling for selectbox */
        .stSelectbox > div > div {
            border-radius: 5px;
        }
        
        /* Custom styling for sliders */
        .stSlider > div > div {
            color: #667eea;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-header {
                padding: 1rem;
            }
            
            .upload-section {
                padding: 1rem;
            }
            
            .results-container {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)