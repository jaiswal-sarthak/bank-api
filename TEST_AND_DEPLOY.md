# 🧪 Test & Deploy - Complete Guide

## Overview

This guide provides comprehensive instructions for testing and deploying the Bank Branches API.

## Testing

### Quick Test

#### 1. Test Setup
```bash
python test_setup.py
```

#### 2. Run Tests
```bash
pytest tests/ -v
```

#### 3. Test with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

#### 4. Test Specific Module
```bash
pytest tests/test_api.py::TestBanksEndpoints -v
```

### Test Results

Expected results:
- ✅ All 31+ tests passing
- ✅ No errors
- ✅ No warnings
- ✅ Complete coverage

### Test Endpoints

#### REST API Tests
- ✅ Root endpoint
- ✅ Health check
- ✅ List banks
- ✅ Get bank details
- ✅ Get bank branches
- ✅ List branches
- ✅ Get branch by IFSC
- ✅ Search branches
- ✅ Filter branches
- ✅ Pagination
- ✅ Statistics

#### GraphQL Tests
- ✅ GraphQL endpoint
- ✅ Query branches
- ✅ Query banks
- ✅ Query specific bank
- ✅ Query specific branch
- ✅ Filters
- ✅ Pagination

#### UI Tests
- ✅ UI endpoint
- ✅ Search functionality
- ✅ Filter functionality
- ✅ GraphQL executor
- ✅ Statistics display

### Manual Testing

#### 1. Start Server
```bash
python run.py
```

#### 2. Test REST API
```bash
# Get all banks
curl http://localhost:8000/api/banks

# Get branch by IFSC
curl http://localhost:8000/api/branches/SBIN0000001

# Search branches
curl "http://localhost:8000/api/branches?bank_name=STATE%20BANK%20OF%20INDIA&city=MUMBAI"

# Get statistics
curl http://localhost:8000/api/stats
```

#### 3. Test GraphQL
```bash
# GraphQL query
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ branches { edges { node { branch ifsc bank { name } } } } }"}'
```

#### 4. Test UI
Open http://localhost:8000/ui in your browser

## Deployment

### Deployment Options

#### 1. Local Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Load data
python scripts/load_data.py

# Start server
python run.py
```

#### 2. Docker Deployment
```bash
# Build image
docker build -t bank-api .

# Run container
docker run -p 8000:8000 bank-api
```

#### 3. Heroku Deployment
```bash
# Create app
heroku create bank-api

# Deploy
git push heroku main

# Load data
heroku run python scripts/load_data.py
```

#### 4. Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

#### 5. Render Deployment
1. Go to https://render.com
2. Create new web service
3. Connect GitHub repository
4. Deploy

### Deployment Checklist

#### Pre-Deployment
- [ ] All tests passing
- [ ] No linter errors
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Environment variables set
- [ ] Database configured
- [ ] Data loaded
- [ ] Security checked

#### Deployment
- [ ] Dependencies installed
- [ ] Database created
- [ ] Data loaded
- [ ] Server running
- [ ] API accessible
- [ ] GraphQL accessible
- [ ] UI accessible
- [ ] Health check passing

#### Post-Deployment
- [ ] API endpoints working
- [ ] GraphQL endpoint working
- [ ] UI accessible
- [ ] Health check passing
- [ ] Statistics working
- [ ] Search working
- [ ] Filters working
- [ ] Pagination working

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

#### 1. Tests Failing
- Check Python version
- Verify dependencies installed
- Review error messages
- Check test database

#### 2. Deployment Errors
- Check logs
- Verify environment variables
- Check database connection
- Review deployment logs

#### 3. API Not Accessible
- Check server running
- Verify port configuration
- Check firewall settings
- Review error logs

#### 4. Data Loading Errors
- Verify CSV file exists
- Check file permissions
- Review error messages
- Check database connection

## Best Practices

### Testing
- Run tests before deployment
- Test all endpoints
- Test edge cases
- Test error handling
- Test performance

### Deployment
- Use environment variables
- Enable HTTPS
- Set up monitoring
- Configure backups
- Set up alerts

### Security
- Use strong passwords
- Enable SSL/TLS
- Restrict access
- Regular updates
- Security audits

## Support

### Resources
- Documentation: `README.md`
- Setup Guide: `README_SETUP.md`
- Installation Guide: `INSTALLATION_GUIDE.md`
- Deployment Guide: `DEPLOYMENT_GUIDE.md`
- API Examples: `API_EXAMPLES.md`

### Troubleshooting
- Check logs
- Review error messages
- Verify configuration
- Test locally
- Check documentation

## Conclusion

This guide provides comprehensive instructions for testing and deploying the Bank Branches API. Follow the steps carefully and refer to troubleshooting section if you encounter issues.

**Happy testing and deploying!** 🚀

