
# CandidateHub – Mini Candidate Job Portal

CandidateHub is a full-stack web application that allows candidates to create accounts, manage their profiles, browse job opportunities, apply for jobs, and track their applications.

The application uses React for the frontend, Python FastAPI for the backend, and PostgreSQL for database management.

## Project Objectives

- Provide candidate registration and login.
- Allow candidates to view and update their profiles.
- Display available job opportunities.
- Support job searching and filtering.
- Allow candidates to apply for jobs.
- Prevent duplicate job applications.
- Allow candidates to track their application status.


## Technology Stack

### Frontend
- React.js
- JavaScript
- HTML
- CSS
- Vite

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Password Hashing

### Database
- PostgreSQL

### Development Tools
- Visual Studio Code
- FastAPI Swagger UI
- Git and GitHub


## Application Features

### 1. Candidate Authentication
- Candidate registration using name, email, and password.
- Secure password hashing.
- Login using email and password.
- JWT-based authentication for protected APIs.

### 2. Candidate Profile
- View candidate profile.
- Update candidate name.
- Access protected profile endpoints.

### 3. Job Listings
- View available jobs.
- Search jobs by title.
- Filter jobs by location.
- Filter jobs by employment type.

### 4. Job Applications
- Apply for available jobs.
- Prevent multiple applications for the same job.
- View previously submitted applications.
- Track application status.


## How to Run the Project Locally

### Prerequisites
- Python installed
- Node.js and npm installed
- PostgreSQL installed

### 1. Clone the Repository

```bash
git clone https://github.com/AfreenTaj12/candidate-hub
cd candidate-hub
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install fastapi sqlalchemy "psycopg[binary]" python-dotenv "pwdlib[argon2]" PyJWT python-multipart email-validator
```

Create a `.env` file inside the backend folder:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
```

Start the backend:

```bash
uvicorn main:app --reload
```

Backend URL: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: http://localhost:5173



## AI-Assisted Development

### AI Tool Used
ChatGPT

### How AI Was Used

I used ChatGPT as a development assistant while building CandidateHub.

- Planned the application structure and backend API endpoints.
- Received guidance while implementing FastAPI routes and database operations.
- Used explanations to understand JWT authentication and password hashing.
- Debugged errors during backend and frontend integration.
- Reviewed API responses and tested features using Swagger UI and the React frontend.

I reviewed the generated code, made changes, and tested the functionality before proceeding.

### Sample AI Prompts

1. "Help me build a candidate job portal using React, FastAPI, and PostgreSQL. Guide me step by step."

2. "Explain how to implement JWT authentication in FastAPI, including password hashing and protected routes."

3. "Help me connect my React frontend to FastAPI APIs for candidate login, job listings, and job applications."

### Testing

- Tested backend APIs using FastAPI Swagger documentation.
- Tested candidate registration and login.
- Verified profile viewing and updating.
- Tested job search and filtering.
- Tested job applications and duplicate application prevention.
- Verified application tracking from the frontend.
