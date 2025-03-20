import spacy
import nltk
import re
import os
from pdfminer.high_level import extract_text

# Load SpaCy NLP Model
nlp = spacy.load("en_core_web_sm")

# Sample Skill Database
skills_db = ["Python", "Java", "Machine Learning", "Data Science", "NLP", "Deep Learning"]


# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""


# Function to Extract Candidate Name (Assumes name is among first few lines)
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":  # Identifies a person name using NLP
            return ent.text
    return "Unknown"  # Default if no name is found


# Function to Extract Skills
def extract_skills(text):
    doc = nlp(text)
    found_skills = [token.text for token in doc if token.text in skills_db]
    return list(set(found_skills))


# Function to Extract Education
def extract_education(text):
    education_keywords = ["Bachelor", "Master", "B.Sc", "M.Sc", "PhD", "B.Tech", "M.Tech"]
    sentences = nltk.sent_tokenize(text)
    education = [sent for sent in sentences if any(keyword in sent for keyword in education_keywords)]
    return education


# Function to Extract Experience
def extract_experience(text):
    exp_pattern = re.compile(r'\b(\d{1,2})\s+(years|year|months|month)\b', re.IGNORECASE)
    matches = exp_pattern.findall(text)

    total_experience = sum(int(match[0]) for match in matches) if matches else 0
    return total_experience


# Function to Process Resume
def process_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    candidate_name = extract_name(text)  # Extract name from PDF
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)

    resume_data = {
        "Name": candidate_name,
        "PDF Number": pdf_path,  # Store PDF file name
        "Score": 5 * experience + 3 * len(skills)  # Score Calculation
    }
    return resume_data



# User Inputs
no_of_candidates_present = int(input("How many candidates have applied? "))
no_of_candidates_to_select = int(input("How many candidates to select? "))

candidates = []

# Automatically process resumes R1.pdf, R2.pdf, ..., RN.pdf
for i in range(1, no_of_candidates_present + 1):
    pdf_path = f"R{i}.pdf"  # Resume files must follow "R<number>.pdf"

    if os.path.exists(pdf_path):  # Check if file exists before processing
        result = process_resume(pdf_path)
        candidates.append(result)
    else:
        print(f"Warning: {pdf_path} not found, skipping...")

# Sort Candidates by Score (Descending)
sorted_candidates = sorted(candidates, key=lambda x: x["Score"], reverse=True)

# Select Top Candidates
selected_candidates = sorted_candidates[:no_of_candidates_to_select]

# Display Final Output (Only Name and PDF Number)
print("\nSelected Candidates:")
for candidate in selected_candidates:
    print(f"Name: {candidate['Name']}, PDF: {candidate['PDF Number']}")
