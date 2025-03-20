#
import spacy
import nltk
import json
import re
from pdfminer.high_level import extract_text

# Load SpaCy NLP Model
nlp = spacy.load("en_core_web_sm")

# Sample Skill Database
skills_db = ["Python", "Java", "Machine Learning", "Data Science", "NLP", "Deep Learning"]

# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

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
    if matches:
        total_experience = sum(int(match[0]) for match in matches)
        return f"{total_experience} years"
    return "Not specified"

# Function to Process Resume
def process_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    skills = extract_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)

    resume_data = {
        "Skills": skills,
        "Education": education,
        "Experience": experience
    }
    return json.dumps(resume_data, indent=4)

# Example Usage
no_of_candidates_present = input("How many candidates have applied?")
no_of_candidates_to_select = input("How many candidates to select?")
pdf_path_type = "R"
pdf_path = "R1.pdf"  # Change this if needed
result = process_resume(pdf_path)
print(result)
score_matrix = []
for i in no_of_candidates_present:
    result = process_resume(pdf_path_type + str(i) + ".pdf")
    ## score of each candidate = 5*experience + 3 * skills

## After score is generated sort the candidates on the score and use no_of_candidates_to_select are the number of candidates to be selected display the according result