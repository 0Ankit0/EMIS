#!/bin/bash
# Integration Test Script for EMIS Frontend + Backend

echo "🧪 EMIS Integration Test Suite"
echo "================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test backend availability
echo -e "\n${YELLOW}1. Testing Backend Availability...${NC}"
BACKEND_URL=${API_BASE_URL:-http://localhost:8000}

if curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health" | grep -q "200"; then
    echo -e "${GREEN}✓ Backend is running at $BACKEND_URL${NC}"
else
    echo -e "${RED}✗ Backend not reachable at $BACKEND_URL${NC}"
    echo "Please start backend with: ./start-dev.sh"
    exit 1
fi

# Test API endpoints
echo -e "\n${YELLOW}2. Testing API Endpoints...${NC}"

# Health check
HEALTH=$(curl -s "$BACKEND_URL/health")
if echo "$HEALTH" | grep -q "status"; then
    echo -e "${GREEN}✓ Health endpoint working${NC}"
else
    echo -e "${RED}✗ Health endpoint failed${NC}"
fi

# API docs
if curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/docs" | grep -q "200"; then
    echo -e "${GREEN}✓ API documentation available at $BACKEND_URL/docs${NC}"
else
    echo -e "${RED}✗ API documentation not available${NC}"
fi

# Test frontend dependencies
echo -e "\n${YELLOW}3. Testing Frontend Dependencies...${NC}"

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python3 installed${NC}"
else
    echo -e "${RED}✗ Python3 not found${NC}"
    exit 1
fi

if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip installed${NC}"
else
    echo -e "${RED}✗ pip not found${NC}"
    exit 1
fi

# Check if streamlit is installed
if python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${GREEN}✓ Streamlit installed${NC}"
else
    echo -e "${YELLOW}⚠ Streamlit not installed${NC}"
    echo "Installing dependencies..."
    pip install -r frontend/requirements.txt
fi

# Test frontend configuration
echo -e "\n${YELLOW}4. Testing Frontend Configuration...${NC}"

if [ -f "frontend/.env" ]; then
    echo -e "${GREEN}✓ .env file exists${NC}"
else
    echo -e "${YELLOW}⚠ .env file not found, using defaults${NC}"
fi

if [ -f "frontend/.streamlit/config.toml" ]; then
    echo -e "${GREEN}✓ Streamlit config exists${NC}"
else
    echo -e "${RED}✗ Streamlit config not found${NC}"
fi

# Test imports
echo -e "\n${YELLOW}5. Testing Python Imports...${NC}"

cd frontend

python3 << EOF
try:
    import streamlit
    import requests
    import pandas
    import plotly
    print("✓ All required packages installed")
except ImportError as e:
    print(f"✗ Import error: {e}")
    exit(1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All imports successful${NC}"
else
    echo -e "${RED}✗ Import errors detected${NC}"
    cd ..
    exit 1
fi

cd ..

# Summary
echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}Integration Tests Complete!${NC}"
echo -e "${GREEN}================================${NC}"

echo -e "\n📋 Next Steps:"
echo "1. Start backend: ./start-dev.sh"
echo "2. Start frontend: cd frontend && ./start-frontend.sh"
echo "3. Open browser: http://localhost:8501"
echo "4. Login with default credentials"

echo -e "\n🔗 Useful URLs:"
echo "- Frontend: http://localhost:8501"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo "- ReDoc: http://localhost:8000/redoc"
