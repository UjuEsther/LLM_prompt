import os
import json
import fitz  # PyMuPDF
from openai import OpenAI
from dotenv import load_dotenv
from llm_prompt import generate_system_prompt

# Load your API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Create OpenAI client instance
client = OpenAI(api_key=api_key)

# All the LLM prompt tasks
TASKS = [
    "paper_metadata",
    "focus_scope",
    "platforms_devices",
    "anti_forensic_techniques",
    "forensic_artifacts",
    "taxonomy_discussion",
    "evaluation_method",
    "contribution_type"

]

# Function to extract full text from a PDF
def extract_pdf_text(file_path):
    doc = fitz.open(file_path)
    return " ".join(page.get_text() for page in doc)

# Process a single paper
def process_paper(pdf_path):
    filename = os.path.basename(pdf_path)
    title_guess = os.path.splitext(filename)[0]
    content = extract_pdf_text(pdf_path)

    paper = {
        "title": title_guess,
        "content": content
    }

    results = {}
    for task in TASKS:
        try:
            prompt = generate_system_prompt(paper, task)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": prompt}]
            )
            results[task] = response.choices[0].message.content
        except Exception as e:
            results[task] = f"Error: {str(e)}"
    
    return results

# Batch process all PDFs in the papers folder
def run_batch():
    input_dir = "papers"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            print(f"Processing {filename}...")
            pdf_path = os.path.join(input_dir, filename)
            result = process_paper(pdf_path)

            output_file = os.path.join(output_dir, f"{filename}.json")
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2)
    print("📄 Scanning papers folder...")

    print("✅ Done processing all papers.")

if __name__ == "__main__":
    run_batch()
