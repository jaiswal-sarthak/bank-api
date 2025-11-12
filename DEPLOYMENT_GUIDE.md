# 🚀 Bank Branches API - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Bank Branches API to various platforms.

## Prerequisites

- Python 3.8+
- Git
- (Optional) Docker
- (Optional) Heroku CLI
- (Optional) PostgreSQL (for production)

## Quick Deployment Options

### 1. Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Load data
python scripts/load_data.py

# Start server
python run.py
```

**Access:**
- REST API: http://localhost:8000/docs
- GraphQL: http://localhost:8000/graphql
- UI: http://localhost:8000/ui

### 2. Docker Deployment

#### Build Image
```bash
docker build -t bank-api .
```

#### Run Container
```bash
docker run -p 8000:8000 bank-api
```

#### With Docker Compose
```bash
docker-compose up
```

#### With Data Loading
```bash
# Build and run with data loading
docker build -t bank-api .
docker run -p 8000:8000 -v $(pwd)/bank_branches.csv:/app/bank_branches.csv bank-api python scripts/load_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Heroku Deployment

#### Step 1: Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Login to Heroku
```bash
heroku login
```

#### Step 3: Create Heroku App
```bash
heroku create bank-api
```

#### Step 4: Set Environment Variables
```bash
# For PostgreSQL (recommended)
heroku addons:create heroku-postgresql:mini

# Get database URL
heroku config:get DATABASE_URL

# Set database URL
heroku config:set DATABASE_URL=<your-database-url>
```

#### Step 5: Deploy
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Deploy to Heroku
git push heroku main
```

#### Step 6: Load Data
```bash
# Load data from CSV
heroku run python scripts/load_data.py
```

#### Step 7: Open App
```bash
heroku open
```

### 4. Railway Deployment

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

#### Step 2: Login
```bash
railway login
```

#### Step 3: Initialize Project
```bash
railway init
```

#### Step 4: Deploy
```bash
railway up
```

#### Step 5: Set Environment Variables
```bash
railway variables set DATABASE_URL=<your-database-url>
```

### 5. Render Deployment

#### Step 1: Create Account
- Go to https://render.com
- Sign up or login

#### Step 2: Create New Web Service
- Click "New" → "Web Service"
- Connect your GitHub repository
- Select the repository

#### Step 3: Configure Service
- **Name**: bank-api
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: Free or Paid

#### Step 4: Set Environment Variables
- `DATABASE_URL`: Your database URL
- `DEBUG`: False

#### Step 5: Deploy
- Click "Create Web Service"
- Wait for deployment to complete

#### Step 6: Load Data
- Go to Shell
- Run: `python scripts/load_data.py`

### 6. DigitalOcean App Platform

#### Step 1: Create Account
- Go to https://www.digitalocean.com
- Sign up or login

#### Step 2: Create App
- Click "Create" → "Apps"
- Connect your GitHub repository
- Select the repository

#### Step 3: Configure App
- **Name**: bank-api
- **Region**: Choose your region
- **Plan**: Basic or Professional

#### Step 4: Set Environment Variables
- `DATABASE_URL`: Your database URL
- `DEBUG`: False

#### Step 5: Deploy
- Click "Create Resources"
- Wait for deployment to complete

#### Step 6: Load Data
- Go to Console
- Run: `python scripts/load_data.py`

### 7. AWS Elastic Beanstalk

#### Step 1: Install EB CLI
```bash
pip install awsebcli
```

#### Step 2: Initialize EB
```bash
eb init -p python-3.11 bank-api
```

#### Step 3: Create Environment
```bash
eb create bank-api-env
```

#### Step 4: Set Environment Variables
```bash
eb setenv DATABASE_URL=<your-database-url> DEBUG=False
```

#### Step 5: Deploy
```bash
eb deploy
```

#### Step 6: Load Data
```bash
eb ssh
python scripts/load_data.py
```

### 8. Google Cloud Run

#### Step 1: Install gcloud CLI
```bash
# Download from https://cloud.google.com/sdk/docs/install
```

#### Step 2: Login
```bash
gcloud auth login
```

#### Step 3: Create Project
```bash
gcloud projects create bank-api
gcloud config set project bank-api
```

#### Step 4: Build and Deploy
```bash
# Build image
gcloud builds submit --tag gcr.io/bank-api/bank-api

# Deploy to Cloud Run
gcloud run deploy bank-api --image gcr.io/bank-api/bank-api --platform managed --region us-central1
```

#### Step 5: Set Environment Variables
```bash
gcloud run services update bank-api --set-env-vars DATABASE_URL=<your-database-url>,DEBUG=False
```

## Environment Variables

### Required Variables
- `DATABASE_URL`: Database connection string
  - SQLite: `sqlite:///./bank_branches.db`
  - PostgreSQL: `postgresql://user:password@host:port/database`

### Optional Variables
- `DEBUG`: Debug mode (default: `False`)
- `PORT`: Port number (default: `8000`)

## Database Setup

### SQLite (Development)
- Default database
- No setup required
- File: `bank_branches.db`

### PostgreSQL (Production)
- Recommended for production
- Setup database:
  ```sql
  CREATE DATABASE bank_branches;
  ```
- Update `DATABASE_URL`:
  ```
  DATABASE_URL=postgresql://user:password@host:port/bank_branches
  ```

### MySQL (Alternative)
- Supported via SQLAlchemy
- Update `DATABASE_URL`:
  ```
  DATABASE_URL=mysql://user:password@host:port/database
  ```

## Data Loading

### Option 1: Automated (Recommended)
- Data loads automatically on deployment (Heroku)
- Configured in `Procfile`

### Option 2: Manual
```bash
python scripts/load_data.py
```

### Option 3: Via Shell
```bash
# Heroku
heroku run python scripts/load_data.py

# Docker
docker exec -it <container-id> python scripts/load_data.py
```

## Monitoring

### Health Check
```bash
curl http://your-api-url/health
```

### Statistics
```bash
curl http://your-api-url/api/stats
```

### Logs
```bash
# Heroku
heroku logs --tail

# Docker
docker logs <container-id>

# Railway
railway logs
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Error
- Check `DATABASE_URL` environment variable
- Verify database is accessible
- Check firewall settings

#### 2. Data Loading Error
- Verify CSV file exists
- Check file permissions
- Review error logs

#### 3. Port Already in Use
- Change port in configuration
- Check if another process is using the port
- Use environment variable `PORT`

#### 4. Dependency Installation Error
- Update pip: `pip install --upgrade pip`
- Check Python version: `python --version`
- Review error messages

#### 5. Deployment Error
- Check logs for errors
- Verify environment variables
- Check database connection
- Review deployment logs

## Best Practices

### 1. Use PostgreSQL for Production
- Better performance
- Better concurrency
- Better scalability

### 2. Set Environment Variables
- Never commit sensitive data
- Use environment variables
- Use secrets management

### 3. Enable HTTPS
- Use SSL/TLS certificates
- Configure reverse proxy
- Use cloud provider SSL

### 4. Monitor Performance
- Use health checks
- Monitor logs
- Set up alerts
- Track metrics

### 5. Backup Data
- Regular database backups
- Version control
- Disaster recovery plan

## Security

### 1. Environment Variables
- Never commit secrets
- Use environment variables
- Use secrets management

### 2. Database Security
- Use strong passwords
- Enable SSL connections
- Restrict access
- Regular backups

### 3. API Security
- Enable HTTPS
- Use authentication (if needed)
- Rate limiting
- Input validation

### 4. Deployment Security
- Use secure connections
- Enable firewall
- Regular updates
- Security audits

## Scaling

### Horizontal Scaling
- Use load balancer
- Multiple instances
- Database replication
- Caching layer

### Vertical Scaling
- Increase resources
- Optimize database
- Use connection pooling
- Cache frequently accessed data

## Cost Optimization

### 1. Use Free Tiers
- Heroku Free Tier
- Railway Free Tier
- Render Free Tier

### 2. Optimize Resources
- Use appropriate instance sizes
- Enable auto-scaling
- Monitor usage
- Optimize database queries

### 3. Use Caching
- Redis caching
- CDN for static files
- Database query caching

## Support

### Resources
- Documentation: `README.md`
- Setup Guide: `README_SETUP.md`
- Build Guide: `BUILD_GUIDE.md`
- API Examples: `API_EXAMPLES.md`

### Troubleshooting
- Check logs
- Review documentation
- Check error messages
- Verify configuration

## Conclusion

This deployment guide provides comprehensive instructions for deploying the Bank Branches API to various platforms. Choose the deployment method that best fits your needs.

**Ready to deploy!** 🚀

