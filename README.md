# Career Services Platform

A comprehensive, professional web platform for career progression services, offering both individual and bundled services for job seekers, executives, and students. Built with a modern tech stack and designed for scalability and performance.

## 🌟 Features

### 👥 User Management
- User registration and authentication
- Profile management with resume/CV upload
- Personalized dashboards
- Role-based access control (admin, staff, client)
- Notification system

### 🛒 Services & Packages
- Service categories and individual services
- Custom service packages with discounts
- Service feature comparison
- Client testimonials and reviews
- Featured services on homepage

### 📝 Content Management
- Blog with categories, tags, and comments
- Rich text editing with CKEditor
- SEO optimization for all content
- Media library for images and documents
- Featured and related posts

### 📅 Appointment System
- Calendar integration
- Time slot management
- Appointment booking and rescheduling
- Email reminders and notifications
- Availability management

### 💳 Payment Processing
- Secure payment via PayPal and Stripe
- Order management
- Invoice generation
- Coupon and discount system
- Subscription management

### 📊 Analytics & Reporting
- User activity tracking
- Service performance metrics
- Financial reporting
- Conversion rate analytics
- Custom dashboard widgets

## 🛠️ Technology Stack

### Frontend
- **Framework**: React.js
- **State Management**: Redux
- **Styling**: Styled Components, Material-UI
- **API Communication**: Axios
- **Form Handling**: Formik, Yup

### Backend
- **Framework**: Django REST Framework
- **Authentication**: JWT, OAuth
- **Task Queue**: Celery
- **Caching**: Redis
- **API Documentation**: drf-yasg (Swagger)

### Database & Storage
- **Primary Database**: PostgreSQL
- **Caching Layer**: Redis
- **File Storage**: AWS S3 (optional)

### DevOps & Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx
- **Process Manager**: Gunicorn
- **CI/CD**: GitHub Actions (planned)
- **Monitoring**: Sentry

### Payment Processing
- PayPal Express Checkout
- Stripe (planned)

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Node.js 16+ (for local frontend development)
- Python 3.9+ (for local backend development)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/career-services-platform.git
   cd career-services-platform
   ```

2. Create environment file
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start the Docker containers
   ```bash
   docker-compose up -d
   ```

4. Access the application
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - API Documentation: http://localhost:8000/api/docs/
   - Admin Dashboard: http://localhost:8000/admin/
   - Celery Flower Dashboard: http://localhost:5555/

### Default Admin Credentials

```
Username: admin
Password: admin
```

## 💻 Development

For detailed development guidelines, architecture overview, and contribution guidelines, see [PROJECT_GUIDE.md](PROJECT_GUIDE.md).

### Local Development

#### Backend
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Frontend
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions or support, please contact [your-email@example.com](mailto:your-email@example.com).

## 🙏 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React](https://reactjs.org/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
