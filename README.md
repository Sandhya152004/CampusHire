# Placement Management Portal

A full-stack web application designed to manage and streamline the campus placement process between students, companies, and the institute placement cell.

The platform provides separate role-based access for Students, Companies, and Admin with secure authentication, placement drive management, application tracking, and recruitment workflow management.

## Features

### Admin
- Secure admin login (pre-created superuser)
- Dashboard with placement statistics
- Approve and manage company registrations
- Manage students, companies, and placement drives
- Role-based access control

### Company
- Company registration and authentication
- Company dashboard
- Create placement drives
- View student applications
- Shortlist, reject, and update application status

### Student
- Student registration and authentication
- View available placement drives
- Eligibility-based applications
- Apply for placement opportunities
- Track application status and placement history
- Profile management support

## Tech Stack

### Frontend
- Vue.js 3
- Vue Router
- Axios
- Bootstrap

### Backend
- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- REST APIs

### Database
- SQLite

### Upcoming Enhancements
- Resume upload
- Advanced search and filtering
- Redis caching
- Celery background jobs
- Daily reminders
- Monthly placement reports
- CSV export

## Project Architecture

Frontend communicates with the Flask backend through REST APIs. Authentication is handled using JWT tokens with role-based authorization for Students, Companies, and Admin.

