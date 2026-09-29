# CampusHire

A full-stack campus placement management platform connecting students,
companies, and placement administrators through role-based workflows.

## Live Demo

Frontend: https://campushire-frontend-hvng.onrender.com/

Backend API: https://campushire-0gko.onrender.com/

## Overview

CampusHire is a role-based placement management system designed to
digitize the campus recruitment process.

The platform provides separate dashboards and workflows for:

- Students
- Companies
- Placement Administrators

The application includes authentication, placement-drive management,
eligibility filtering, applications, shortlisting, interview scheduling,
resume management, and reporting.

## Features

### Student

- Student registration and login
- Profile management
- Resume upload
- Browse placement drives
- Search placement drives
- Filter by degree and eligibility
- Skill-match indicators
- Apply for placement drives
- Withdraw applications
- Track application status
- Change password

### Company

- Company registration and authentication
- Company profile management
- Create placement drives
- Define eligibility criteria
- Specify required skills
- View applicants
- Shortlist or reject candidates
- Schedule interviews

### Admin

- Admin authentication
- Manage students and companies
- Manage placement drives
- Monitor applications
- Manage recruitment workflows
- Generate reports

## Tech Stack

### Frontend

- Vue.js 3
- Vue Router
- Axios
- Bootstrap
- Vite

### Backend

- Python
- Flask
- Flask REST APIs
- SQLAlchemy
- JWT Authentication
- Flask-Caching

### Database & Infrastructure

- PostgreSQL
- SQLite for local development
- Redis
- Celery
- Docker
- Render

## Architecture

```text
                    ┌────────────────────┐
                    │   Vue.js Frontend  │
                    │   Render Static    │
                    │       Site         │
                    └─────────┬──────────┘
                              │
                              │ REST API
                              ▼
                    ┌────────────────────┐
                    │   Flask Backend    │
                    │    Render Web      │
                    │      Service       │
                    └──────┬─────┬───────┘
                           │     │
                 ┌─────────┘     └─────────┐
                 ▼                         ▼
          ┌──────────────┐          ┌──────────────┐
          │ PostgreSQL   │          │    Redis     │
          │   Database   │          │    Cache     │
          └──────────────┘          └──────┬───────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │    Celery    │
                                    │ Background   │
                                    │    Tasks     │
                                    └──────────────┘
