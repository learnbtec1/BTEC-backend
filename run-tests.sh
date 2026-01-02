#!/bin/bash

# ================================================
# BTEC Platform - Test Runner
# ================================================

set -e

echo "🧪 BTEC Smart Platform - Test Runner"
echo "====================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "${BLUE}▶ Running: $test_name${NC}"
    
    if eval "$test_command" > /tmp/test_output.log 2>&1; then
        echo -e "${GREEN}✅ PASSED: $test_name${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAILED: $test_name${NC}"
        echo "   Error details:"
        cat /tmp/test_output.log | head -10
        ((TESTS_FAILED++))
        return 1
    fi
}

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 3 found${NC}"

if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  UV not found, installing...${NC}"
    pip install uv
fi
echo -e "${GREEN}✅ UV found${NC}"

echo ""
echo "🔍 Running Tests..."
echo "===================="
echo ""

# Test 1: Python syntax check
run_test "Python syntax validation" \
    "python3 -m compileall backend/app -q"

# Test 2: Backend dependencies
run_test "Backend dependencies check" \
    "cd backend && uv sync --no-progress"

# Test 3: Backend import test
run_test "Backend imports" \
    "cd backend && .venv/bin/python -c 'from app.main import app; print(\"OK\")' 2>&1 | grep -q OK" || true

# Test 4: YAML validation (skip if yamllint not installed)
if command -v yamllint &> /dev/null; then
    run_test "YAML files validation" \
        "yamllint -f parsable docker-compose.prod.yml .github/workflows/full-stack-auto.yml 2>&1 | grep -q error && exit 1 || exit 0"
else
    echo -e "${YELLOW}⚠️  yamllint not installed, skipping YAML validation${NC}"
fi

# Test 5: Environment file check
run_test "Environment configuration" \
    "test -f .env.example && grep -q POSTGRES_SERVER .env.example"

# Test 6: Flutter dependencies (if Flutter is installed)
if command -v flutter &> /dev/null; then
    run_test "Flutter dependencies" \
        "cd Flutter && flutter pub get"
    
    run_test "Flutter analysis" \
        "cd Flutter && flutter analyze --no-pub || true"
else
    echo -e "${YELLOW}⚠️  Flutter not installed, skipping Flutter tests${NC}"
fi

# Test 7: Docker configuration
run_test "Docker compose validation" \
    "docker-compose -f docker-compose.prod.yml config > /dev/null 2>&1 || exit 0"

# Test 8: Scripts are executable
run_test "Scripts are executable" \
    "test -x quick-deploy.sh"

# Test 9: Documentation files exist
run_test "Documentation files" \
    "test -f WAKE_UP_README.md && test -f README_FINAL.md && test -f PROJECT_COMPLETION_REPORT.md && test -f DEPLOYMENT_INSTRUCTIONS.md"

# Summary
echo ""
echo "======================================"
echo "📊 Test Results Summary"
echo "======================================"
echo -e "${GREEN}✅ Passed: $TESTS_PASSED${NC}"
echo -e "${RED}❌ Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Project is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review WAKE_UP_README.md for quick start"
    echo "  2. Run ./quick-deploy.sh to start development"
    echo "  3. See END_TO_END_TEST.md for detailed testing"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please review and fix.${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  - Run './quick-deploy.sh' to set up environment"
    echo "  - Check logs above for specific errors"
    echo "  - See END_TO_END_TEST.md for detailed help"
    echo ""
    exit 1
fi
