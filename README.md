# Blue Coding Take Home

## Project Requirements Checklist

### API Requirements

- [x] Implement a method to map user input data to the appropriate fields in various EHR systems, with flexibility for different data types and systems.
- [x] Ensure transactions captured by the API are correctly written to the respective users in the EHRs (e.g., with validation and error handling).
- [x] Use a modular design or standard interface to allow for easy addition of new EHR integrations without significant code changes.
- [x] Design (but do not implement) an API architecture plan that allows for scalability as more users are added (e.g., load balancing, efficient data structures).
- [x] Implement a system for managing field mappings per EHR integration (via DB or config files) and expose methods for CRUD operations on those mappings.
- [x] Implement performance enhancements (e.g., caching, indexing, optimized queries) to ensure scalability.
- [x] Design a testing strategy for the API.
- [x] **Bonus:** Implement the testing strategy using tools like pytest or DRF test client.
- [ ] **Bonus:** Support multi-language question and answer submission (e.g., Spanish and English).

### Frontend Requirements

- [x] Create an internal UI to allow team members to manage mappings for each EHR system.
- [x] Implement proper error handling and user feedback for invalid or failed form submissions.
- [x] Design a testing strategy for the frontend.
- [x] **Bonus:** Implement frontend tests (e.g., React Testing Library with Jest).
- [ ] **Bonus:** Support multi-language UI (e.g., i18n for English/Spanish).
- [ ] **Bonus:** Allow bulk updates for patients under a specific provider or hospital.

## Project Structure

project-root/   
├── backend/ # Django API   
├──── api/ # API directory   
│ ├────── migrations/ # Database migrations  
│ ├────── admin.py # Django admin interface   
│ ├────── apps.py # Django apps   
│ ├────── models.py # Database models  
│ ├────── permissions.py # Permissions  
│ ├────── serializers.py # Data serialization   
│ ├────── tasks.py # Celery tasks  
│ ├────── tests.py # Automated tests   
│ └────── viewsets.py # Django viewsets  
│ ├── ehrintegrator/ # Django project directory   
│ ├────── asgi.py # ASGI entry point  
│ ├────── celery.py # Celery configuration  
│ ├────── settings.py # Django settings  
│ ├────── urls.py # URL configuration  
│ └────── wsgi.py # WSGI entry point  
├── frontend/ # React
│ ├── src/ # React source code
│ │ ├── components/ # Application UI components
│ │ ├── config/ # Configuration files
│ │ ├── pages/ # Pages files
│ │ ├── tests/ # Tests
│ │ ├── App.tsx # Application file
│ │ ├── App.css # Application CSS file
│ │ ├── index.css # Generic CSS file
│ │ ├── main.tsx # React entry point
│ ├── package.json # Frontend application dependencies fil
├──── Dockerfile # Dockerfile for build  
├──── manage.py # Django management commands  
├──── requirements.txt # Python dependencies file  
├── README.md #   git 
└── docker-compose.yml # Docker Compose to orchestrate start up  

## Requirements

- Docker
- Docker Compose

## Project Setup

1. Clone this repository

```bash
git clone https://github.com/omarcosalberto/bluecoding-take-home.git
```

2. Enter the project directory

```bash
cd blue-coding-take-home
```

3. Copy `env-example` to `.env` (optional)

```bash
cp env-example .env
```

4. Run project

```bash
docker compose up
```

5. Create admin user

```bash
docker compose exec -e DJANGO_SUPERUSER_PASSWORD=<password> backend python manage.py createsuperuser --no-input --username <username> --email <email>
```

5. Load sample data (turn test easy)

```bash
docker compose exec backend python manage.py loaddata sample_data.json
```

5. Access admin area

[http://localhost:8000/admin/](http://localhost:8000/admin/)

5. Access form list

[http://localhost:8000/](http://localhost:8000/)