import os
from langchain_community.chat_models import ChatOpenAI
from extract_text import extract_text
from config import OPENAI_API_KEY

# Ensure OpenAI API key is set
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Load extracted text
contract_text = extract_text("contract.pdf")
guidelines_text = extract_text("guideline.pdf")

# Split guidelines into individual rules (assuming each guideline is on a new line)
guidelines = [g.strip() for g in guidelines_text.split("\n") if g.strip()]
# Initialize LangChain OpenAI model
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

def check_compliance(guideline):
    """Checks if a guideline is being followed in the contract."""
    prompt = (
        f"Guideline: {guideline}\n"
        f"Contract: {contract_text}\n\n"
        "Is this guideline being followed in the contract? Answer only 'YES' or 'NO'."
    )
    response = llm.invoke(prompt).content.strip()
    return response

# Check each guideline and print results
for i, guideline in enumerate(guidelines, 1):
    result = check_compliance(guideline)
    print(f"Guideline {i}: {result}")
