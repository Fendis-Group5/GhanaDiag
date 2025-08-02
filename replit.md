# Overview

This is a medical diagnostic web application designed specifically for Ghana, providing automated health assessments based on symptoms. The system helps users identify potential medical conditions by analyzing their symptoms and provides relevant recommendations and next steps. It focuses on common conditions in Ghana such as malaria, typhoid, and influenza, using a rule-based diagnostic engine to provide preliminary health guidance.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a traditional server-side rendered architecture with Flask templates and modern styling:
- **Template Engine**: Jinja2 templates with a modular design using template inheritance
- **Styling Framework**: Tailwind CSS with a custom "winter chill" color theme
- **Interactive Elements**: Vanilla JavaScript for form enhancements, theme management, and dynamic user interactions
- **Responsive Design**: Mobile-first approach with responsive grid layouts and adaptive components

## Backend Architecture
The backend follows a simple Flask MVC pattern:
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Application Structure**: Modular design with separate files for models, routes, and the diagnostic engine
- **Session Management**: Flask sessions with configurable secret keys
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

## Data Storage Solutions
- **Primary Database**: SQLite for development with PostgreSQL support via environment configuration
- **ORM**: SQLAlchemy with DeclarativeBase for modern Python data modeling
- **Connection Management**: Connection pooling with health checks and automatic reconnection
- **Data Models**: Two main entities - Submissions (patient assessments) and Feedback (user feedback on diagnosis accuracy)

## Diagnostic Engine
- **Rule-Based System**: Custom diagnostic engine implementing condition-specific symptom matching
- **Condition Database**: JSON-based storage of medical conditions with symptoms, severity indicators, and recommendations
- **Symptom Processing**: Handles both structured symptom selection and free-text symptom descriptions
- **Localized Content**: Tailored for common conditions in Ghana with region-specific medical guidance

## User Interface Features
- **Multi-Step Assessment**: Personal information collection, symptom selection, and diagnosis presentation
- **Example Symptom Bundles**: Pre-defined symptom combinations to guide user input
- **Assessment History**: Historical tracking of user assessments and outcomes
- **Feedback System**: User feedback collection to improve diagnostic accuracy over time
- **Accessibility**: ARIA labels, keyboard navigation, and screen reader support

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web application framework and routing
- **SQLAlchemy**: Database ORM and connection management
- **Werkzeug**: WSGI utilities and proxy handling

## Frontend Dependencies
- **Tailwind CSS**: Utility-first CSS framework via CDN
- **Feather Icons**: SVG icon library for consistent iconography
- **Custom CSS**: Additional styling for theme management and component enhancement

## Database Support
- **SQLite**: Default development database (file-based)
- **PostgreSQL**: Production database support via DATABASE_URL environment variable
- **Connection Pooling**: Built-in SQLAlchemy connection pool management

## Deployment Configuration
- **Environment Variables**: Support for SESSION_SECRET and DATABASE_URL configuration
- **WSGI Compatibility**: Production-ready with proxy support for reverse proxy deployments
- **Debug Mode**: Configurable debug settings for development vs production environments