from langchain.prompts import PromptTemplate

# 2.1 CVs.pdf -> JSON 
cv_formatting_prompt = PromptTemplate(
    input_variables=["cv_text"],
    template="""
    Extract the following information from the CV text below and output in JSON:
    - Full Name
    - Email
    - Phone
    - Skills
    - Education (degree, institution, year)
    - Experience (role, company, duration, description)
    - Certifications (if any)
    - Projects (if any)
    CV Text:
    {cv_text}
    """
)

# 2.2 Job description.pdf -> JSON
jd_formatting_prompt = PromptTemplate(
    input_variables=["jd_text"],
    template="""
    Extract the following information from the job description below and output it in **JSON** format.

    The structure should be similar to the CV JSON format so that comparison can be done easily later.

    Specifically include these fields:
    - Job Title
    - Company
    - Location
    - Employment Type (e.g., Full-time, Hybrid, Remote)
    - Role Summary
    - Responsibilities (list)
    - Required Qualifications (list)
    - Preferred Qualifications (list)
    - Skills (list)
    - Education Requirements
    - Experience Requirements
    - Certifications (if any)
    - Offered Benefits (if any)

    Job Description:
    {jd_text}
    """
)


comparison_prompt = PromptTemplate(
    input_variables=["job_description", "candidates"],
    template="""
You are an expert hiring assistant. 
Compare the following job description and candidate profiles.

Job Description:
{job_description}

Candidates (in JSON format):
{candidates}

For each candidate:
- Analyze skills, education, and experience relevant to the job.
- Provide a suitability score from 0 to 100.
- Briefly explain the reasoning.
But don't show this analysis only show this a table with the canditates sorted 
from the highest rank to the lowest, for each candidate retunr the name, score, and reason. 
    """
)

