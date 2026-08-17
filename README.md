# Job-Portal
# 💼 Django Job Portal System

A **Django-based Job Portal and Recruitment Management System** that connects **Recruiters** with **Jobseekers**.

Recruiters can create company profiles, post job opportunities, define required skills, set application deadlines, and manage job openings. Jobseekers can create professional profiles, upload resumes, view available jobs, and apply for suitable positions.

---

## ✨ Features

### 👤 User Management

The project uses a custom Django user model based on `AbstractUser`.

There are two types of users:

* 🏢 **Recruiter**
* 👨‍💼 **Jobseeker**

Each user type has a dedicated profile.

---

### 🏢 Recruiter Management

Recruiters can create and manage company profiles containing:

* Company name
* Company address
* Contact information
* Company logo
* Account creation date
* Profile update date

Recruiter profiles are connected to the custom user model using a `OneToOneField`.

---

### 👨‍💼 Jobseeker Management

Jobseekers can create professional profiles containing:

* Name
* Profile image
* Address
* Skill set
* Resume
* Profile creation date
* Profile update date

Jobseekers can use their profiles when applying for jobs.

---

### 📂 Job Category Management

Jobs can be organized into different categories.

For example:

```text
Software Development
Marketing
Accounting
Human Resources
Graphic Design
Sales
Customer Support
```

Each category contains a category name.

---

### 💼 Job Posting

Recruiters can post job vacancies with information such as:

* Job title
* Number of openings
* Job category
* Recruiter/company
* Job description
* Required skills
* Application deadline
* Creation date
* Last update date

Each job post is associated with a specific recruiter and category.

---

### 📄 Job Application

Jobseekers can apply for available jobs.

Each application contains:

* Applicant
* Applied job
* Resume
* Application date

The system connects the jobseeker with the job post through the application model.

---

# 🏗️ System Architecture

The main relationship between the models is:

```text id="1v6k39"
                         UserModel
                        /         \
                       /           \
                Recruiter       Jobseeker
                    │                │
                    ▼                ▼
          RecruitersModel       SeekeerModel
                    │                │
                    │                │
                    ▼                ▼
             JobPostModel       ApplyJobModel
                    │                │
                    ├───────┐        │
                    ▼       │        │
             categoryModel  │        │
                            └────────┘
```

---

# 🔗 Model Relationships

### User → Recruiter

```text id="z0w3q5"
UserModel
    │
    └── RecruitersModel
          One-to-One
```

### User → Jobseeker

```text id="q3r6s2"
UserModel
    │
    └── SeekeerModel
          One-to-One
```

### Recruiter → Jobs

```text id="e3d7tq"
RecruitersModel
       │
       └── JobPostModel
             One-to-Many
```

### Category → Jobs

```text id="5j2y8n"
categoryModel
       │
       └── JobPostModel
             One-to-Many
```

### Jobseeker → Applications

```text id="9p3b4h"
SeekeerModel
       │
       └── ApplyJobModel
             One-to-Many
```

### Job → Applications

```text id="x8s1fv"
JobPostModel
       │
       └── ApplyJobModel
             One-to-Many
```

---

# 🧰 Technologies Used

* **Python**
* **Django**
* **Django ORM**
* **SQLite / PostgreSQL**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Bootstrap** *(if used)*
* **Pillow** for image uploads

---

# 📁 Main Models

## 👤 `UserModel`

Custom authentication model extending Django's `AbstractUser`.

Available user types:

```text id="6x9l5z"
Recruiters
Jobseekers
```

Additional fields:

```text id="c8u3sy"
display_name
user_type
```

---

## 🏢 `RecruitersModel`

Stores recruiter/company information.

Fields:

```text id="5g1d8q"
recruiter
company_name
address
contract
logo
created_at
updated_at
```

Each recruiter is connected to one `UserModel`.

---

## 👨‍💼 `SeekeerModel`

Stores jobseeker information.

Fields:

```text id="1w2m8k"
seeker
name
profile_image
address
skill_set
resume
created_at
updated_at
```

The jobseeker can upload a resume and provide their skills and personal information.

---

## 📂 `categoryModel`

Stores job categories.

Fields:

```text id="f7k2za"
name
```

Categories are used to organize job postings.

---

## 💼 `JobPostModel`

Stores job vacancy information.

Fields:

```text id="6jv4tx"
title
numer_of_opening
category
post_by
desciption
skill_set
deadline
created_at
updated_at
```

Each job post belongs to:

* One category
* One recruiter

---

## 📄 `ApplyJobModel`

Stores job application information.

Fields:

```text id="v8n5rc"
applied_by
applied_job
resume
applied_at
```

Each application connects:

```text
Jobseeker → Job
```

---

# 🔄 Application Workflow

The general workflow of the system is:

```text id="q0r2kx"
                    RECRUITER
                       │
                       ▼
                Create Company Profile
                       │
                       ▼
                 Create Job Post
                       │
                       ▼
               Add Job Information
                       │
                       ▼
                 Publish Job
                       │
                       ▼
                     JOB
                       │
                       ▼
                   JOBSEEKER
                       │
                       ▼
                Create Profile
                       │
                       ▼
                 Upload Resume
                       │
                       ▼
                 Browse Jobs
                       │
                       ▼
                 Select Job
                       │
                       ▼
                 Apply for Job
                       │
                       ▼
               Application Created
```

---

# 📄 Resume Management

Jobseekers can upload their resumes using Django's `FileField`.

The profile contains:

```python id="9d7g5w"
resume = models.FileField(null=True)
```

Job applications can also contain a resume:

```python id="4q7s2m"
resume = models.FileField(null=True)
```

This allows an applicant to submit a resume when applying for a specific job.

---

# 🖼️ Profile & Company Images

The project supports image uploads for both recruiters and jobseekers.

### Company Logo

```python id="y7r4z8"
logo = models.ImageField(
    upload_to='company_logo',
    null=True
)
```

### Jobseeker Profile Image

```python id="m5w2cx"
profile_image = models.ImageField(
    upload_to='seeker_image',
    null=True
)
```

Make sure Pillow is installed:

```bash id="f1z8cp"
pip install pillow
```

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash id="r7w1sq"
git clone https://github.com/your-username/your-repository-name.git
```

Navigate to the project:

```bash id="9n3t5d"
cd your-repository-name
```

---

## 2. Create a Virtual Environment

### Windows

```bash id="m7x4vq"
python -m venv venv
```

Activate the environment:

```bash id="8k2fws"
venv\Scripts\activate
```

### Linux / macOS

```bash id="z4p6nb"
python3 -m venv venv
```

Activate:

```bash id="j9c5rx"
source venv/bin/activate
```

---

## 3. Install Dependencies

If `requirements.txt` is available:

```bash id="b6v3qa"
pip install -r requirements.txt
```

Otherwise:

```bash id="e4q9mc"
pip install django pillow
```

Create the requirements file:

```bash id="u3w7zn"
pip freeze > requirements.txt
```

---

# 🔐 Configure Custom User Model

Because this project uses a custom user model, add the following to `settings.py`:

```python id="k2d8py"
AUTH_USER_MODEL = 'your_app_name.UserModel'
```

For example:

```python id="s6n4bf"
AUTH_USER_MODEL = 'accounts.UserModel'
```

Replace `accounts` with your actual Django application name.

> **Important:** Set `AUTH_USER_MODEL` before creating your initial migrations whenever possible, because changing the user model after migrations/data exist can require additional migration work.

---

# 🗂️ Configure Media Files

Since the project supports company logos, profile images, and resumes, configure media files in `settings.py`:

```python id="w4q7kj"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Then add media URL handling to your project's `urls.py`:

```python id="n3p8xc"
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your URL patterns
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
```

---

# 🗄️ Database Setup

Create migrations:

```bash id="t7m2va"
python manage.py makemigrations
```

Apply migrations:

```bash id="r5c8yx"
python manage.py migrate
```

---

# 👨‍💼 Create Superuser

Create an admin account:

```bash id="p9v4kc"
python manage.py createsuperuser
```

Enter your username, email, and password.

Then access Django Admin:

```text id="s2j6qw"
http://127.0.0.1:8000/admin/
```

---

# ▶️ Run the Project

Start the Django development server:

```bash id="g8x1mz"
python manage.py runserver
```

Open:

```text id="d4n7hb"
http://127.0.0.1:8000/
```

---

# 📊 Example Job Post

A recruiter can create a job such as:

```text id="p1x7cd"
Job Title:
Python Django Developer

Category:
Software Development

Number of Openings:
3

Required Skills:
Python, Django, REST API, PostgreSQL

Description:
We are looking for a Django developer
to join our development team.

Application Deadline:
2026-09-30
```

---

# 📋 Example Job Application

A jobseeker can apply with:

```text id="u8s4nk"
Applicant:
John Doe

Job:
Python Django Developer

Resume:
john_doe_resume.pdf

Applied At:
2026-08-11
```

---

# 🔐 Security Recommendations

Before deploying this project to production:

* Set `DEBUG = False`
* Use a secure `SECRET_KEY`
* Configure `ALLOWED_HOSTS`
* Store secrets in environment variables
* Use PostgreSQL or another production database
* Enable HTTPS
* Configure static and media files properly
* Add role-based permissions
* Restrict recruiter-only functionality
* Restrict jobseeker-only functionality
* Validate uploaded resume files
* Validate uploaded image files
* Prevent unauthorized users from modifying job posts
* Prevent users from accessing private applicant information

Example `.gitignore`:

```text id="w5j3az"
venv/
__pycache__/
*.pyc
db.sqlite3
.env
media/
staticfiles/
```

---

# 🔮 Future Improvements

The project can be extended with:

* 🔍 Job search
* 🎯 Advanced job filtering
* 📍 Location-based job search
* 💰 Salary range
* 🏠 Remote / Hybrid / On-site job type
* 📊 Recruiter dashboard
* 📋 Applicant management
* 📧 Application email notifications
* 🔔 Real-time notifications
* 📈 Recruitment analytics
* ⭐ Company ratings
* 💬 Recruiter-applicant messaging
* 📄 Resume preview
* 📥 Resume download
* 🔖 Save/bookmark jobs
* ❤️ Favorite jobs
* 📊 Application status tracking
* 📝 Interview scheduling
* 📅 Interview management
* 🔐 Advanced role-based permissions
* 🌐 Django REST Framework API
* 📱 Responsive mobile UI

---

# 📂 Recommended Project Structure

```text id="y5p9bw"
job-portal/
│
├── manage.py
│
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── jobs/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── templates/
│
├── static/
│
├── media/
│   ├── company_logo/
│   └── seeker_image/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🤝 Contributing

Contributions are welcome!

### 1. Fork the repository

### 2. Create a feature branch

```bash id="x4c7pn"
git checkout -b feature/new-feature
```

### 3. Make your changes

### 4. Commit your changes

```bash id="n8y2kr"
git add .
git commit -m "Add new feature"
```

### 5. Push the branch

```bash id="c5m9vz"
git push origin feature/new-feature
```

### 6. Open a Pull Request

---

# 📄 License

This project is developed for **educational and development purposes**.

You can add an **MIT License** or another open-source license according to your requirements.

---

# 👨‍💻 Author

**Oren Michael Dessai**

If you find this project useful, please ⭐ the repository on GitHub.

---
