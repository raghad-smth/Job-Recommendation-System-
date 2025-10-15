# Job Recommendation System

**An intelligent job matching application** powered by **LangChain** and **Google’s Gemini model via OpenRouter API**.
This system analyzes candidate CVs and a job description, extracts structured data, and provides a **compatibility score (0–100)** along with reasoning for each candidate.

---

<img width="1369" height="874" alt="image" src="https://github.com/user-attachments/assets/fc33f1c3-4de5-4c85-aa0b-dcaec7895632" />

## Project Structure

The project consists of **three main Python files** and a **sample data folder**:

| File / Folder                | Description                                                                                                                                                                                                                                                                                                                                                      |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`Loading.py`](./Loading.py) | Handles loading of PDFs and the OpenRouter API key. Includes a function to extract text from PDFs and store it as strings, and loads the API key securely from an environment variable.                                                                                                                                                                          |
| [`Prompts.py`](./Prompts.py) | Stores all the **LLM prompts** used by the system — including prompts for:<br>• Formatting CVs into JSON<br>• Formatting Job Descriptions into JSON<br>• Comparing candidates with the job description                                                                                                                                                           |
| [`main.py`](./main.py)       | The main **Streamlit app** where all the logic is brought together. It loads the LLM, defines the chains for CV and JD processing, evaluates candidates, and displays everything with custom CSS for a clean interface.                                                                                                                                          |
| `Candidates/`                | Contains sample candidate CVs and job descriptions for testing:<br>• `Perfect_candidate.pdf` → expected high score (90–100)<br>• `Bad_candidate.pdf` → not related to the job<br>• `Omar_Khaled_AlmostFit.pdf` → expected around 70/100<br>• `Sara_ElMasry_PartialFit.pdf` → expected around 35/100<br>• `ML_JD.pdf` → Machine Learning Engineer job description |

---

## How It Works

The system runs in **three main stages**:

1. **CV Formatting**
   Each uploaded CV PDF is converted to structured JSON using the `cv_formatting_prompt`.

2. **Job Description Formatting**
   The job description PDF is processed into structured JSON using the `jd_formatting_prompt`.

3. **Candidate Evaluation**
   Each formatted CV is compared against the job description using the `comparison_prompt`.
   The model outputs a **Markdown table** with:

   * Candidate Name
   * Suitability Score (0–100)
   * Explanation for the score

---

## Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/job-recommendation-system.git
cd job-recommendation-system
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv jrs
source jrs/bin/activate  # For macOS/Linux
jrs\Scripts\activate     # For Windows
```

### 3️⃣ Install Dependencies

The main libraries used:

* `streamlit`
* `langchain`
* `langchain-openai`
* `pypdf` or `PyMuPDF` (for PDF text extraction)

---

## API Key Setup

Before running the app, you must create an **OpenRouter API key**:

1. Visit [https://openrouter.ai/](https://openrouter.ai/) and sign up.
2. Copy your API key.
3. Create a `.env` file in your project root directory containing:

   ```
   OPEN_ROUTER_API_Key=your_api_key_here
   ```

This key allows you to access the **Gemini LLM** through the OpenRouter endpoint.

---

## 🚀 Running the Application

Once everything is set up, simply run:

```bash
streamlit run main.py
```

Then open the URL displayed in your terminal (usually `http://localhost:8501`).

---

## How to Use

1. **Upload a Job Description (PDF)**
   e.g., `ML_JD.pdf` (Machine Learning Engineer role)

2. **Upload Candidate CVs (PDFs)**
   e.g., `Perfect_candidate.pdf`, `Bad_candidate.pdf`, `Omar_Khaled_AlmostFit.pdf`, etc.

3. Click **Run Evaluation**
   
Image of the final output:
<img width="1223" height="717" alt="image" src="https://github.com/user-attachments/assets/4183c1af-0dda-42a6-a343-64232777d1b0"/>
---
