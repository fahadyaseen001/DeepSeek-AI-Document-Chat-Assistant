# DeepSeek AI Document Chat Assistant 🤖

A streamlined document chat application powered by DeepSeek-R1 that allows users to upload documents and engage in natural conversations about their content. This application supports PDF, DOCX, and image files, making it versatile for various document types.

## Features ✨

- **Document Processing**: Upload and process PDF, DOCX, and image files
- **Text Extraction**: Automatic text extraction from various file formats
- **Interactive Chat**: Natural conversation interface for document queries
- **Real-time Processing**: Live document analysis and response generation
- **Clean UI**: Simple and intuitive Streamlit interface
- **File Support**: Handles multiple document formats with size limit checks

## Requirements 📋

```
streamlit
together
pdfplumber
python-docx
pytesseract
Pillow
pdf2image
```

## Setup & Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/fahadyaseen001/DeepSeek-AI-Document-Chat-Assistant.git
cd DeepSeek-AI-Document-Chat-Assistant
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR (required for image processing):
- For Ubuntu/Debian:
  ```bash
  sudo apt-get install tesseract-ocr
  ```
- For macOS:
  ```bash
  brew install tesseract
  ```
- For Windows:
  Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

4. Add required images:
- Place `deepseek-color.png` in the root directory

5. Get your API key:
- Sign up at [Together.ai](https://together.ai)
- Generate an API key from your dashboard

## Usage 💡

1. Run the application:
```bash
streamlit run app.py
```

2. In your web browser:
- Enter your Together API key in the sidebar
- Upload a document (PDF, DOCX, or image)
- Wait for processing completion
- Start asking questions about your document

## Supported File Types 📄

- PDF documents (`.pdf`)
- Word documents (`.docx`)
- Images (`.png`, `.jpg`, `.jpeg`)

## Size Limits 📏

- Maximum file size: 200MB
- Maximum text processing: 6000 characters per query

## Architecture 🏗️

The application is built with the following components:

- **Frontend**: Streamlit web interface
- **Document Processing**: pdfplumber, python-docx, pytesseract
- **AI Model**: DeepSeek-R1 via Together API
- **Session Management**: Streamlit session state

## Development 👨‍💻

To contribute to the project:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Repository Description 📝

```
DeepSeek AI Document Chat Assistant: An intelligent document analysis tool powered by DeepSeek-R1. Upload documents and chat naturally about their contents. Supports PDFs, Word documents, and images with an intuitive interface built using Streamlit.

Key features:
• Multi-format document support
• Natural language document queries
• Real-time processing
• Clean, user-friendly interface
• Powered by DeepSeek-R1 AI
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- DeepSeek-R1 model by DeepSeek
- Together.ai for API access
- Streamlit for the web framework
- Various open-source libraries used in the project