# Django Online Job Portal with RAG Match

A comprehensive job portal application built with Django, featuring a cutting-edge **RAG (Retrieval-Augmented Generation)** based job relevancy scoring system.

## 🚀 Features

### For Candidates (Student Users)
- **Profile Management**: Register and manage user profiles.
- **Job Search**: Browse and search for latest job postings.
- **RAG Job Match**: Instantly compare your resume against job descriptions to get:
  - **Match Score**: A percentage indicating relevancy.
  - **Skill Analysis**: List of matching and missing skills.
  - **Insights**: Strengths and a detailed relevancy explanation.
- **Application Tracking**: Apply to jobs with resume uploads.

### For Recruiters
- **Company Branding**: Manage recruiter profile and company details.
- **Job Management**: Create, edit, and manage job postings.
- **Candidate Review**: View a list of candidates who applied for jobs.
- **Recruiter Dashboard**: Manage active job listings.

### For Administrators
- **User Management**: Approve or reject recruiter registrations.
- **Global Overview**: Monitor all users and job activities.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (Development)
- **AI/ML (RAG Pipeline)**:
  - **LLM**: Groq (Llama-3.1-8b-instant)
  - **Vector Store**: FAISS
  - **Embeddings**: Sentence Transformers
  - **Framework**: LangChain
- **Frontend**: HTML5, CSS3, Vanilla JS

## 📋 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/codegeekyyy/online-job-portal.git
   cd django-online-job-portal
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## 🔐 Authentication Guide
- **Admin**: Create a superuser via `python manage.py createsuperuser` and access `/admin/`.
- **Recruiter**: Sign up via `/recruitersignup/` and wait for admin approval.
- **Candidate**: Sign up via `/usersignup/`.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
