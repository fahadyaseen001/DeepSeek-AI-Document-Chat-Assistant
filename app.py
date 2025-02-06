import streamlit as st
from together import Together
import pdfplumber
from docx import Document
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io
import base64

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image not found: {image_path}")
        return ""

# Get base64 encoded logos
DEEPSEEK_LOGO = get_base64_image("deepseek-color.png")
POWERED_LOGO = get_base64_image("deepseek-color.png")  # Using same logo for powered by section

def extract_text(file_bytes, file_type):
    text = ""
    try:
        if file_type == "application/pdf":
            try:
                with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                if text.strip():
                    return text
            except:
                images = convert_from_bytes(file_bytes)
                for image in images:
                    text += pytesseract.image_to_string(image)
        
        elif file_type in ["image/png", "image/jpeg"]:
            image = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(image)
        
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs])
            
        return text.strip()
    
    except Exception as e:
        st.error(f"Text extraction failed: {str(e)}")
        return ""

def chat_with_document(api_key, text, question):
    if not api_key:
        st.error("Please enter your Together API Key")
        return ""
    
    client = Together(api_key=api_key)
    
    prompt = f"""You are a helpful AI assistant. Analyze the document below and answer the question.
If the answer cannot be found in the document, respond only with: "This information is not present in the document."
Keep your response concise and direct. Do not include any explanations about your thinking process.

Document:
{text[:6000]}

Question: {question}

Answer:"""
    
    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Chat failed: {str(e)}")
        return ""

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def reset_chat_state():
    st.session_state.messages = []
    if 'document_text' in st.session_state:
        del st.session_state.document_text

def main():
    st.set_page_config(
        page_title="DeepSeek AI Document Chat Assistant",
        layout="wide",
        page_icon="deepseek-color.png"
    )
    
    initialize_chat_history()
    
    with st.sidebar:
        st.markdown("## API Configuration")
        api_key = st.text_input(
            "Enter Together API Key:", 
            type="password",
            help="Get your API key from Together.ai"
        )
        st.markdown("[Get API Key →](https://together.ai)")
        
        st.divider()
        
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="data:image/png;base64,{POWERED_LOGO}" style="width: 30px; height: auto;"/>
                <span>Powered by DeepSeek-R1</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Title with DeepSeek logo
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{DEEPSEEK_LOGO}" style="height: 50px; width: auto;"/>
            <h1 style="margin: 0; font-size: 2.5rem;">DeepSeek AI Document Chat Assistant</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if 'previous_file' not in st.session_state:
        st.session_state.previous_file = None

    uploaded_file = st.file_uploader(
        "Upload your document",
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        help="Supported formats: PDF, DOCX, PNG, JPG, JPEG (Max: 200MB)"
    )

    if st.session_state.previous_file is not None and uploaded_file is None:
        reset_chat_state()
    
    st.session_state.previous_file = uploaded_file

    if uploaded_file and api_key:
        if uploaded_file.size > 200 * 1024 * 1024:
            st.error("File size exceeds 200MB limit")
            return
            
        if 'document_text' not in st.session_state:
            with st.spinner("Processing document..."):
                text = extract_text(uploaded_file.getvalue(), uploaded_file.type)
                if not text:
                    st.error("Failed to process document")
                    return
                st.session_state.document_text = text
                st.success("Ready to chat!")
    
    if 'document_text' in st.session_state:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if question := st.chat_input("Ask a question about your document..."):
            with st.chat_message("user"):
                st.markdown(question)
            st.session_state.messages.append({"role": "user", "content": question})
            
            with st.chat_message("assistant"):
                with st.spinner("Processing..."):
                    response = chat_with_document(api_key, st.session_state.document_text, question)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    else:
        st.info("Upload a document and provide your API key to start chatting!")

if __name__ == "__main__":
    main()