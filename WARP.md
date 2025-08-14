# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Nino Medical AI** is an open-source medical AI research platform built with Streamlit. It provides both free and Pro versions, featuring authentication systems, medical database integrations, and AI analysis capabilities for the healthcare sector.

## Development Environment Setup

### Environment Requirements
- **Python**: 3.11.7 (specified in user rules)
- **Package Manager**: Anaconda (preferred installation method per user rules)
- **Framework**: Streamlit (primary framework per user rules)

### Quick Setup
```bash
# Create conda environment (recommended)
conda create -n nino-medical-ai python=3.11.7
conda activate nino-medical-ai

# Install dependencies
pip install -r requirements.txt
```

### Anaconda Installation (User Preference)
Install Anaconda with these specific options (per user rules):
- JustMe installation
- RegisterPython=1
- AddToPath=1
- Silent installation

## Common Development Commands

### Running the Application
```bash
# Main Streamlit app
streamlit run nino_medical_ai_app.py

# Alternative entry points for different versions
streamlit run simple_medical_ai_app.py           # Simple version
streamlit run basic_medical_ai_app.py            # Basic version
streamlit run nino_medical_enhanced_simple.py   # Enhanced simple version
```

### Building Executables
```bash
# Build all versions (Windows batch)
build_all.bat

# Build optimized version
python build_optimized.py

# Build Pro desktop version
python build_pro.py

# Build version without imaging
python build_desktop_pro.py
```

### Testing and Validation
```bash
# Test protection system
python test_protection_system.py

# Run individual build scripts
python build_imaging.bat      # With imaging capabilities
python build_no_imaging.bat   # Without imaging capabilities
```

## Architecture Overview

### Core Application Structure
The project follows a modular architecture with distinct separation between:

1. **Authentication Layer** (`auth_system.py`)
   - User management with role-based access (Guest, User, Admin)
   - Session management with JWT tokens
   - Secure password hashing with bcrypt

2. **Licensing System** (`pro_license_system.py`)
   - Feature protection via decorators
   - Pro feature access validation
   - License key generation and verification

3. **Main Application** (`nino_medical_ai_app.py`)
   - Multi-tier user interface (Anonymous, Free, Pro)
   - Protected Pro features with conversion prompts
   - Google Analytics integration

### Key Components

#### Authentication System
- Uses SQLite databases (`auth/users.db`, `auth/licenses.db`)
- Role-based access control with UserRole enum
- Session management with secure tokens

#### Pro Feature Protection
```python
@ProFeatureGuard.require_pro_feature('advanced_ai_analysis')
def protected_function():
    # Pro-only functionality
```

#### Medical Database Integrations
- Multiple medical databases: PubMed, WHO, FDA, UniProt, ClinicalTrials.gov
- Free tier limitations vs. unlimited Pro access
- Built-in demo functionality for conversion

## Development Workflows

### Adding New Pro Features
1. Define feature in `ProFeatureGuard.PRO_FEATURES`
2. Apply `@ProFeatureGuard.require_pro_feature()` decorator
3. Add corresponding free/demo version
4. Update pricing information in UI

### Authentication Development
- User creation requires validation of email and password strength
- All user data is stored in encrypted local SQLite databases
- Session state managed through `SessionManager`

### Building and Distribution
- **Desktop Pro Version**: Saved locally as 'Nino Medical AI Pro' (per user rules)
- **Build Format**: Single executable (.exe) for Windows
- **Optimization**: Significant size reduction achieved (52% smaller builds)

## Docker Deployment

### Local Development
```bash
# Quick start
docker-compose up -d

# With monitoring
docker-compose --profile monitoring up -d

# Production with proxy
docker-compose --profile production up -d
```

### Health Checks
```bash
# Application health
curl -f http://localhost:8501/_stcore/health

# Container logs
docker logs -f nino-medical-ai
```

## Security Considerations

### Data Protection
- No real patient data in repository - uses synthetic/demo data
- GDPR/HIPAA compliant design patterns
- Secure secret management via environment variables

### Authentication Security
- bcrypt password hashing with random salts
- HMAC-SHA256 signed license keys
- Rate limiting on login attempts
- Session timeout management

## Analytics and Monitoring

### Google Analytics Integration
- Page view tracking with engagement metrics
- Feature usage analytics (free vs. pro)
- Conversion funnel monitoring
- Custom event tracking for medical interactions

### Performance Monitoring
- Redis caching for improved performance
- PostgreSQL for structured data persistence
- Health check endpoints for monitoring

## Contributing Guidelines

### Code Standards
- Python 3.11.7+ compatibility
- PEP 8 style guidelines
- Type hints where applicable
- Comprehensive docstrings

### Medical Compliance
- Educational/research purposes only
- No real clinical decision making
- Proper medical disclaimers required
- Cite peer-reviewed sources for medical content

### Testing Requirements
- Unit tests for new functionality
- Protection system validation via `test_protection_system.py`
- Medical data validation with synthetic datasets

## Deployment Targets

### Streamlit Cloud (Demo/Public)
- Repository: GitHub integration
- Main file: `nino_medical_ai_app.py`
- Secrets: Configure authentication keys

### Local Desktop (Pro)
- Single executable deployment
- Local database storage
- Offline capability for sensitive environments

### Enterprise/Cloud
- Docker containerization
- Multi-service orchestration
- Scalable architecture with load balancing

## Important Notes

### User Preferences (From Rules)
- Primary framework: Streamlit
- Python version: 3.11.7
- Anaconda preferred with specific installation options
- Pro version: Local desktop executable, single file

### Medical Disclaimer
This software is for educational, demonstrative, and research purposes only. Never use for real medical diagnoses or clinical decisions. Always consult qualified healthcare professionals.

## Support and Documentation

- **Primary Contact**: ninomedical.ai@gmail.com
- **Repository**: https://github.com/NinoF840/curriculum-streamlit
- **Documentation**: See README.md, CONTRIBUTING.md, DEPLOY_GUIDE.md
- **Build Optimization**: See BUILD_OPTIMIZATIONS.md for performance details
