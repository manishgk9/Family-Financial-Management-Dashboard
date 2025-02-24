# Family Financial Management Dashboard Backend

This is the backend for the Family Financial Management Dashboard, a full-stack platform designed to help family businesses manage their financial assets, transactions, documents, and notifications efficiently. Built with Django and Django REST Framework, it uses JWT authentication for secure access and provides role-based permissions, AI-driven insights, and seamless integration with a frontend application.

## Table of Contents

- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Dependencies](#dependencies)
- [Notes](#notes)

## Project Overview

The backend supports:

- **User Management**: Role-based access (Admin, Family Member, Accountant) with JWT authentication.
- **Financial Asset Tracking**: Manage bank accounts, properties, businesses, and securities.
- **Family Dashboard**: Aggregated financial data.
- **Document Management**: Store and manage documents with file uploads.
- **Transaction Monitoring**: Track and categorize transactions.
- **Selective Data Sharing**: Customizable permissions per user.
- **AI-Driven Insights**: Budget recommendations and expense trends.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   Install Dependencies:
   Ensure you have Python 3.8+ installed, then:
   bash
   pip install -r requirements.txt
   If no requirements.txt exists, install:
   bash
   pip install django djangorestframework djangorestframework-simplejwt pandas
   Configure Environment:
   INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'core',
   ]
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   Set up your database (default SQLite or configure PostgreSQL).
   Apply Migrations:
   bash
   python manage.py makemigrations
   python manage.py migrate
   Create Superuser (for admin access):
   bash
   python manage.py createsuperuser
   Run the Server:
   bash
   python manage.py runserver
   The API will be available at http://127.0.0.1:8000/.
   API Endpoints
   All endpoints are prefixed with /api/ unless otherwise noted. Use Authorization: Bearer <access_token> for authenticated requests.
   Endpoint
   Method
   Description
   Authentication Required
   /
   GET
   Simple index page (optional)
   No
   /auth/login/
   POST
   Login and get tokens
   No
   /auth/refresh/
   POST
   Refresh access token
   No
   /users/
   POST
   Register a new user
   Yes (Admin)
   /users/<uuid:id>/
   GET/PUT
   Get or update user details
   Yes
   /groups/
   GET/POST
   List or create family groups
   Yes (Admin)
   /groups/<uuid:group_id>/permissions/
   PUT
   Update group permissions
   Yes (Admin)
   /assets/
   GET/POST
   List or create assets
   Yes
   /assets/<uuid:id>/
   GET/PUT
   Get or update an asset
   Yes
   /dashboard/
   GET
   Get dashboard data
   Yes
   /transactions/
   GET/POST
   List or create transactions
   Yes
   /documents/
   GET/POST
   List or upload documents
   Yes
   /documents/<uuid:id>/
   GET/PUT
   Get or update a document
   Yes
   /notifications/
   GET
   List user notifications
   Yes
   /notifications/<uuid:id>/
   PUT
   Update a notification (e.g., mark read)
   Yes
   /insights/budget/
   GET
   Get budget recommendations
   Yes
   /insights/trends/
   GET
   Get expense trends
   Yes
   Usage Examples
   ```
1. Login
   Request:
   bash
   curl -X POST http://127.0.0.1:8000/api/auth/login/ \
   -H "Content-Type: application/json" \
   -d '{"email": "user@example.com", "password": "yourpassword"}'
   Response (200 OK):
   json
   {
   "refresh": "<refresh_token>",
   "access": "<access_token>",
   "user": {
   "id": "uuid",
   "email": "user@example.com",
   "role": "family_member",
   "first_name": "John",
   "last_name": "Doe",
   "date_joined": "2025-02-24T12:00:00Z",
   "profile_img": null
   }
   }
   Error (401 Unauthorized):
   json
   {"error": "Invalid email or password."}
1. Refresh Token
   Request:
   bash
   curl -X POST http://127.0.0.1:8000/api/auth/refresh/ \
   -H "Content-Type: application/json" \
   -d '{"refresh": "<refresh_token>"}'
   Response (200 OK):
   json
   {"access": "<new_access_token>"}
1. Register User (Admin Only)
   Request:
   bash
   curl -X POST http://127.0.0.1:8000/api/users/ \
   -H "Content-Type: application/json" \
   -H "Authorization: Bearer <access_token>" \
   -d '{"email": "newuser@example.com", "password": "newpassword", "role": "family_member", "first_name": "Jane", "last_name": "Doe"}'
   Response (201 Created):
   json
   {
   "id": "uuid",
   "email": "newuser@example.com",
   "role": "family_member",
   "first_name": "Jane",
   "last_name": "Doe",
   "date_joined": "2025-02-24T12:05:00Z",
   "profile_img": null
   }
1. Get Assets
   Request:
   bash
   curl -X GET http://127.0.0.1:8000/api/assets/ \
   -H "Authorization: Bearer <access_token>"
   Response (200 OK):
   json
   [
   {
   "id": "uuid",
   "group": {"id": "uuid", "name": "Family A", "admin": {...}, "created_at": "..."},
   "type": "bank_account",
   "name": "Savings",
   "value": "124500.00",
   "last_updated": "2025-02-24T12:00:00Z",
   "api_source": null
   },
   ...
   ]
1. Create Asset
   Request:
   bash
   curl -X POST http://127.0.0.1:8000/api/assets/ \
   -H "Authorization: Bearer <access_token>" \
   -H "Content-Type: application/json" \
   -d '{"type": "property", "name": "House", "value": "450000.00"}'
   Response (201 Created):
   json
   {
   "id": "uuid",
   "group": {...},
   "type": "property",
   "name": "House",
   "value": "450000.00",
   "last_updated": "2025-02-24T12:10:00Z",
   "api_source": null
   }
1. Upload Document
   Request (using multipart/form-data):
   bash
   curl -X POST http://127.0.0.1:8000/api/documents/ \
   -H "Authorization: Bearer <access_token>" \
   -F "name=Will" \
   -F "type=will" \
   -F "file=@/path/to/will.pdf"
   Response (201 Created):
   json
   {
   "id": "uuid",
   "group": {...},
   "name": "Will",
   "file": "http://127.0.0.1:8000/media/documents/will.pdf",
   "file_url": "http://127.0.0.1:8000/media/documents/will.pdf",
   "type": "will",
   "expiry_date": null,
   "uploaded_at": "2025-02-24T12:15:00Z"
   }
1. Get Dashboard Data
   Request:
   bash
   curl -X GET http://127.0.0.1:8000/api/dashboard/ \
   -H "Authorization: Bearer <access_token>"
   Response (200 OK):
   json
   {
   "total_asset_value": "574500.00",
   "recent_transactions": [{...}, {...}],
   "notifications": [{...}, {...}]
   }
1. Get Budget Insights
   Request:
   bash
   curl -X GET http://127.0.0.1:8000/api/insights/budget/ \
   -H "Authorization: Bearer <access_token>"
   Response (200 OK):
   json
   {
   "total_income": "5000.00",
   "total_expense": "-649.99",
   "recommended_budget": "4000.00"
   }
   Dependencies
   Python 3.8+
   Django
   djangorestframework
   djangorestframework-simplejwt
   pandas (for AI insights)
   Install via:
   bash
   pip install django djangorestframework djangorestframework-simplejwt pandas
   Notes
   Authentication: Use the access token in the Authorization header for all protected endpoints. Refresh it with /auth/refresh/ when it expires (default: 15 minutes).
   File Uploads: Documents are stored in the local filesystem under /media/documents/.
   AI Insights: Requires pandas for TrendInsightView. Install it or simplify the view if not needed.
   Error Handling: Expect detailed error messages (e.g., {"error": {...}}) for invalid requests.
   Admin Access: Use the Django admin panel (/admin/) or API to create initial users and groups.
   For further assistance, refer to the code in views.py, serializers.py, and urls.py.

---

### Explanation of `README.md`

- **Setup Instructions**: Guides a developer through installation and configuration, including database setup and running the server.
- **API Endpoints**: Lists all endpoints with their methods, purposes, and authentication requirements in a table.
- **Usage Examples**: Provides `curl` commands for key endpoints (login, refresh, assets, documents, dashboard, insights), showing request/response formats.
- **Dependencies**: Specifies required Python packages.
- **Notes**: Highlights important details like token usage, file storage, and dependencies.

---

### Integration with Your Project

**Test Examples**: Use the provided `curl` commands or adapt them for your React frontend (e.g., with `fetch` or `axios`).
