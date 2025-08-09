# 📄 InvoiceVision

A modern Streamlit application for extracting structured data from invoice images using Qwen 2.5 VL via OpenRouter API.

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🤖 **AI-Powered Extraction** - Uses Qwen 2.5 VL model via OpenRouter
- 📱 **Modern UI** - Responsive design with custom styling
- 📊 **Multiple Export Formats** - JSON and CSV export options
- 🔧 **Configurable** - Select which fields to extract
- 🎯 **Accurate** - Advanced vision model for precise data extraction
- 🔒 **Secure** - Environment-based API key management

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/shagatomte19/InvoiceVision.git
cd InvoiceVision
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key

**Option A: Streamlit Secrets (Recommended)**
```bash
mkdir .streamlit
```
Create `.streamlit/secrets.toml`:
```toml
OPENROUTER_API_KEY = "your_openrouter_api_key_here"
OPENROUTER_SITE_URL = "https://github.com/shagatomte19/invoice-ocr-extractor"
OPENROUTER_SITE_NAME = "Invoice OCR Extractor"
```

**Option B: Environment Variable**
```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

### 4. Get OpenRouter API Key
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up/login
3. Go to API Keys section
4. Create new API key
5. Copy the key

### 5. Run Application
```bash
streamlit run main.py
```

## 📁 Project Structure

```
invoice_ocr_app/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                # Git ignore rules
├── .streamlit/
│   └── secrets.toml          # Streamlit secrets (not in repo)
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration settings
├── api/
│   ├── __init__.py
│   └── openrouter_client.py  # OpenRouter API client
├── utils/
│   ├── __init__.py
│   ├── image_processor.py    # Image processing utilities
│   ├── data_parser.py        # Data parsing and validation
│   └── export_utils.py       # Export functionality
├── ui/
│   ├── __init__.py
│   ├── styles.py             # CSS styles
│   ├── components.py         # Reusable UI components
│   └── layout.py             # Page layout components
└── models/
    ├── __init__.py
    └── invoice_model.py      # Invoice data models
```

## 🎯 Usage

1. **Start Application**: `streamlit run main.py`
2. **Configure API**: Enter OpenRouter API key (if not using secrets)
3. **Upload Invoice**: Select PNG, JPG, or JPEG image
4. **Extract Data**: Click "Extract Data" button
5. **Review Results**: View structured data extraction
6. **Export**: Download as JSON or CSV

## 🛠️ Configuration

### Supported Models
- `qwen/qwen2.5-vl-72b-instruct:free` (Default, Free tier)
- `qwen/qwen2.5-vl-7b-instruct`
- `qwen/qwen2.5-vl-3b-instruct`

### Extraction Options
- ✅ Vendor Information (name, address, phone, email)
- ✅ Invoice Details (number, date, due date)
- ✅ Financial Data (subtotal, tax, total)
- ✅ Line Items (description, quantity, price)

## 🔒 Security

- API keys are never committed to repository
- Uses Streamlit secrets for secure deployment
- Input validation and error handling
- No data stored permanently

## 🐛 Troubleshooting

**API Key Issues:**
- Verify OpenRouter API key is valid
- Check API key has sufficient credits
- Ensure proper configuration in secrets.toml

**File Upload Issues:**
- Supported formats: PNG, JPG, JPEG
- Ensure image quality is good
- Check file size (recommend < 5MB)

**Deployment Issues:**
- Verify all dependencies in requirements.txt
- Check Python version compatibility (3.8+)
- Ensure .streamlit/secrets.toml is configured

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## ⭐ Support

If you find this project helpful, please give it a star! ⭐

## 📞 Contact

- GitHub Issues: [Report bugs or request features](https://github.com/yourusername/invoice-ocr-extractor/issues)
- Discussions: [Community discussions](https://github.com/yourusername/invoice-ocr-extractor/discussions)

---

**Built with ❤️ using Streamlit and Qwen 2.5 VL**
