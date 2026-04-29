
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import pdfplumber

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LATEST_DATA = {}

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text

def parse_ooc_pdf(pdf_path):
    text = extract_text(pdf_path)
    return {
        "invoices": [{"invoice_no": "INV001", "amount": 1000}],
        "items": [{"item_description": "Sample Item", "assess_value": 500, "total_duty": 50}]
    }

@app.post("/upload")
async def upload(file: UploadFile):
    global LATEST_DATA
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        pdf_path = tmp.name
    LATEST_DATA = parse_ooc_pdf(pdf_path)
    return {"status": "success"}

@app.get("/data")
def get_data():
    return LATEST_DATA
