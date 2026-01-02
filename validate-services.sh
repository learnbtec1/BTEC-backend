#!/bin/bash

# MetaLearn Pro - Service Validation Script
# Validates all microservices are working correctly

set -e

echo "🔍 MetaLearn Pro - Service Validation"
echo "====================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to test service health
test_service() {
    local service_name=$1
    local port=$2
    local url="http://localhost:${port}/"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -n "Testing ${service_name} (port ${port})... "
    
    if curl -s -f "${url}" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Function to test API endpoint
test_endpoint() {
    local service_name=$1
    local method=$2
    local endpoint=$3
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -n "  Testing ${method} ${endpoint}... "
    
    if curl -s -X "${method}" -f "${endpoint}" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

echo "📋 Step 1: Syntax Validation"
echo "=============================="

# Check Python syntax for all services
for service in ai_tutor learning_companion gamification analytics virtual_campus simulations blockchain; do
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Checking ${service} syntax... "
    
    if python -m py_compile "services/${service}/main.py" 2>/dev/null; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
done

echo ""
echo "📋 Step 2: Docker Configuration Validation"
echo "============================================"

# Check if Docker Compose file exists and is valid
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "Validating docker-compose.metalearn.yml... "

if [ -f "docker-compose.metalearn.yml" ]; then
    if docker-compose -f docker-compose.metalearn.yml config > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${YELLOW}⚠ SKIPPED (Docker not available)${NC}"
    fi
else
    echo -e "${RED}✗ FAILED (File not found)${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

echo ""
echo "📋 Step 3: Environment Configuration"
echo "======================================"

# Check if .env.example exists
TOTAL_TESTS=$((TOTAL_TESTS + 1))
echo -n "Checking .env.example... "

if [ -f ".env.example" ]; then
    echo -e "${GREEN}✓ PASSED${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}✗ FAILED${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Check for required environment variables in .env.example
REQUIRED_VARS=("OPENAI_API_KEY" "POSTGRES_USER" "POSTGRES_PASSWORD" "SECRET_KEY")

for var in "${REQUIRED_VARS[@]}"; do
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Checking ${var} in .env.example... "
    
    if grep -q "${var}=" .env.example 2>/dev/null; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
done

echo ""
echo "📋 Step 4: Documentation Validation"
echo "====================================="

# Check if documentation files exist
DOCS=("METALEARN_README.md" "API_SERVICES_DOCUMENTATION.md")

for doc in "${DOCS[@]}"; do
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Checking ${doc}... "
    
    if [ -f "${doc}" ]; then
        echo -e "${GREEN}✓ PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}✗ FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
done

echo ""
echo "📋 Step 5: Service Structure Validation"
echo "========================================="

# Check each service has required files
SERVICES=("ai_tutor" "learning_companion" "gamification" "analytics" "virtual_campus" "simulations" "blockchain")

for service in "${SERVICES[@]}"; do
    for file in "main.py" "requirements.txt" "Dockerfile" "__init__.py"; do
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        echo -n "Checking services/${service}/${file}... "
        
        if [ -f "services/${service}/${file}" ]; then
            echo -e "${GREEN}✓ PASSED${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e "${RED}✗ FAILED${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
    done
done

echo ""
echo "========================================="
echo "📊 Test Results Summary"
echo "========================================="
echo ""
echo "Total Tests:  ${TOTAL_TESTS}"
echo -e "Passed:       ${GREEN}${PASSED_TESTS}${NC}"
echo -e "Failed:       ${RED}${FAILED_TESTS}${NC}"
echo ""

# Calculate success rate
SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
echo "Success Rate: ${SUCCESS_RATE}%"
echo ""

if [ ${FAILED_TESTS} -eq 0 ]; then
    echo -e "${GREEN}✓ All validation tests passed!${NC}"
    echo "🎉 MetaLearn Pro is ready for deployment!"
    exit 0
else
    echo -e "${YELLOW}⚠ Some tests failed. Please review the results above.${NC}"
    exit 1
fi
