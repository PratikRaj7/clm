import os
import fitz  # PyMuPDF
import pdfplumber
import pytesseract
import cv2
import numpy as np
from PIL import Image
from langchain_openai import OpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from config import OPENAI_API_KEY  # Import API key from config.py
from typing import Dict

# LangChain LLM Configuration
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)  # Now using imported API key

# PDF Extraction Class
class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def is_scanned(self):
        """Check if the PDF is scanned by analyzing the first page"""
        with pdfplumber.open(self.pdf_path) as pdf:
            first_page = pdf.pages[0]
            return not first_page.extract_text()

    def ocr_extract(self):
        """Extract text from scanned PDF using OCR"""
        text = ""
        doc = fitz.open(self.pdf_path)
        for page_num in range(len(doc)):
            img = doc[page_num].get_pixmap()
            img_array = np.frombuffer(img.samples, dtype=np.uint8).reshape(img.h, img.w, img.n)
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            text += pytesseract.image_to_string(pil_img)
        return text

    def extract_text(self):
        """Extract text from the PDF using PyMuPDF or OCR if needed"""
        if self.is_scanned():
            print(f"📄 {self.pdf_path} is a scanned document, using OCR...")
            return self.ocr_extract()
        else:
            print(f"📄 Extracting text from {self.pdf_path} using PyMuPDF...")
            text = ""
            with fitz.open(self.pdf_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text

# Simplified extraction function
def extract_text_from_pdfs(guideline_path, contract_path):
    """Extract text from PDFs and report extraction status"""
    print("\n🔍 Starting Extraction Process...\n")
    
    extraction_results = {
        "guideline": {"success": False, "text": None},
        "contract": {"success": False, "text": None}
    }
    
    try:
        # Extract guideline text
        guideline_extractor = PDFExtractor(guideline_path)
        guideline_text = guideline_extractor.extract_text()
        extraction_results["guideline"] = {
            "success": bool(guideline_text),
            "text": guideline_text
        }
        
        # Extract contract text
        contract_extractor = PDFExtractor(contract_path)
        contract_text = contract_extractor.extract_text()
        extraction_results["contract"] = {
            "success": bool(contract_text),
            "text": contract_text
        }
        
    except Exception as e:
        print(f"\n❌ Error during extraction: {str(e)}")
        return extraction_results
    
    print("\n✅ Extraction Complete!")
    return extraction_results

# Simplified Tool
def extract_text_tool(inputs):
    if isinstance(inputs, str):
        import ast
        try:
            inputs = ast.literal_eval(inputs)
        except (SyntaxError, ValueError):
            raise ValueError(f"Invalid input format received: {inputs}")

    if not isinstance(inputs, dict):
        raise TypeError(f"Expected inputs to be a dictionary but received: {type(inputs)}")

    guideline_path, contract_path = inputs.get("guideline"), inputs.get("contract")
    
    if not guideline_path or not contract_path:
        raise ValueError("Both 'guideline' and 'contract' paths are required!")

    return extract_text_from_pdfs(guideline_path, contract_path)

# Update Tool Setup
extraction_tool = Tool(
    name="PDFExtractionAgent",
    func=extract_text_tool,
    description="Extracts text from PDFs and reports extraction status."
)

# Initialize LangChain Agent (Updated)
extraction_agent = initialize_agent(
    tools=[extraction_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Updated AgentType
    verbose=True
)

def process_extracted_texts(texts: Dict[str, str]):
    """Process the texts extracted by the PDFQueryService"""
    print("\n🤔 Thought: Starting analysis of extracted texts")
    
    extraction_results = {
        "guideline": {"success": False, "text": None},
        "contract": {"success": False, "text": None}
    }
    
    try:
        # Process guideline text
        guideline_text = texts.get("guideline")
        if guideline_text:
            extraction_results["guideline"] = {
                "success": True,
                "text": guideline_text
            }
            print("\n👀 Observation: Successfully received guideline text")
            print("\n📋 GUIDELINE TEXT:")
            print("=" * 80)
            print(guideline_text)
            print("=" * 80)
        
        # Process contract text
        contract_text = texts.get("contract")
        if contract_text:
            extraction_results["contract"] = {
                "success": True,
                "text": contract_text
            }
            print("\n👀 Observation: Successfully received contract text")
            print("\n📄 CONTRACT TEXT:")
            print("=" * 80)
            print(contract_text)
            print("=" * 80)
        
        # Add final thoughts and observations
        print("\n🤔 Final Thought: All texts have been processed and analyzed.")
        print("\n👀 Final Observation: Text processing complete. Full texts displayed above.")
        
        return extraction_results
    
    except Exception as e:
        print(f"\n🤔 Thought: An error occurred during processing")
        print(f"\n👀 Observation: Error details - {str(e)}")
        return extraction_results

if __name__ == "__main__":
    # This section now serves as a fallback for direct PDF processing
    print("\n🤔 Thought: Starting direct PDF extraction process")
    input_files = {"guideline": "guideline.pdf", "contract": "contract.pdf"}
    
    try:
        print("\n👀 Observation: Processing input files:", input_files)
        extraction_results = extract_text_tool(input_files)
        
        print("\n🤔 Thought: Generating final report")
        # Report extraction status
        for doc_type, result in extraction_results.items():
            status = "✅ Success" if result["success"] else "❌ Failed"
            print(f"\n👀 Observation: {doc_type.title()} Extraction: {status}")
            if result["success"]:
                print(f"Preview: {result['text'][:200]}...")
        
        # Add final thoughts and observations
        print("\n🤔 Final Thought: All extraction tasks completed. Both documents have been processed.")
        print("\n👀 Final Observation: The extraction process has finished. Check the success status for each document above to confirm successful extraction.")
    
    except Exception as e:
        print(f"\n🤔 Thought: An error occurred during execution")
        print(f"\n👀 Observation: Error details - {str(e)}")
        

        
# guideline

# contract 

# look at gudeline, scan though relevant parts of contract ,if match found then ok ,check if al aspects are matching  
