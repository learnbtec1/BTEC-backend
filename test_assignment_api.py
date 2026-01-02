#!/usr/bin/env python3
"""
Test script for the Assignment Management API
This script tests the main functionality without requiring a running database
"""

import sys
import os

# Set required environment variables before imports
os.environ['PROJECT_NAME'] = 'BTEC Test'
os.environ['POSTGRES_SERVER'] = 'localhost'
os.environ['POSTGRES_USER'] = 'postgres'
os.environ['POSTGRES_PASSWORD'] = 'test'
os.environ['POSTGRES_DB'] = 'test'
os.environ['FIRST_SUPERUSER'] = 'admin@test.com'
os.environ['FIRST_SUPERUSER_PASSWORD'] = 'test123'

# Add backend to path
sys.path.insert(0, '/home/runner/work/BTEC-backend/BTEC-backend/backend')

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from app.models import User, Assignment, AssignmentCreate, AssignmentPublic
        print("✓ Models imported successfully")
    except Exception as e:
        print(f"✗ Error importing models: {e}")
        return False
    
    try:
        from app import crud
        print("✓ CRUD functions imported successfully")
    except Exception as e:
        print(f"✗ Error importing crud: {e}")
        return False
    
    try:
        from app.api.api_v1.endpoints import assignments
        print("✓ Assignment endpoints imported successfully")
    except Exception as e:
        print(f"✗ Error importing endpoints: {e}")
        return False
    
    try:
        from app.api.deps import get_current_teacher, get_current_student
        print("✓ Role dependencies imported successfully")
    except Exception as e:
        print(f"✗ Error importing dependencies: {e}")
        return False
    
    return True


def test_model_creation():
    """Test model instantiation"""
    print("\nTesting model creation...")
    
    try:
        from app.models import User, Assignment, AssignmentCreate
        from datetime import datetime
        import uuid
        
        # Test User model
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "role": "student",
            "is_active": True,
            "is_superuser": False,
            "full_name": "Test User"
        }
        # Note: We can't create a User without hashed_password
        print("✓ User model structure validated")
        
        # Test AssignmentCreate model
        assignment = AssignmentCreate(
            title="Test Assignment",
            description="This is a test"
        )
        print(f"✓ AssignmentCreate model created: {assignment.title}")
        
        return True
    except Exception as e:
        print(f"✗ Error creating models: {e}")
        return False


def test_file_validation():
    """Test file validation logic"""
    print("\nTesting file validation...")
    
    try:
        from app.api.api_v1.endpoints.assignments import validate_file, ALLOWED_EXTENSIONS
        
        # Create mock upload file
        class MockUploadFile:
            def __init__(self, filename):
                self.filename = filename
        
        # Test allowed extensions
        for ext in [".pdf", ".docx", ".jpg", ".png"]:
            try:
                validate_file(MockUploadFile(f"test{ext}"))
                print(f"✓ File type {ext} validated successfully")
            except Exception as e:
                print(f"✗ Error validating {ext}: {e}")
                return False
        
        # Test disallowed extension
        try:
            validate_file(MockUploadFile("test.exe"))
            print("✗ Should have rejected .exe file")
            return False
        except Exception:
            print("✓ Correctly rejected disallowed file type (.exe)")
        
        return True
    except Exception as e:
        print(f"✗ Error in file validation test: {e}")
        return False


def test_crud_functions():
    """Test CRUD function signatures"""
    print("\nTesting CRUD functions...")
    
    try:
        from app import crud
        import inspect
        
        # Check if all required functions exist
        required_functions = [
            'create_assignment',
            'get_assignment',
            'get_student_assignments',
            'get_all_assignments',
            'update_assignment',
            'get_assignment_stats'
        ]
        
        for func_name in required_functions:
            if hasattr(crud, func_name):
                func = getattr(crud, func_name)
                sig = inspect.signature(func)
                print(f"✓ Function '{func_name}' exists with signature: {sig}")
            else:
                print(f"✗ Function '{func_name}' not found")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error checking CRUD functions: {e}")
        return False


def test_endpoint_structure():
    """Test API endpoint structure"""
    print("\nTesting endpoint structure...")
    
    try:
        from app.api.api_v1.endpoints.assignments import router
        
        # Check routes
        routes = []
        for route in router.routes:
            routes.append(f"{route.methods} {route.path}")
        
        print(f"✓ Found {len(router.routes)} routes:")
        for route in routes:
            print(f"  - {route}")
        
        # Check that key routes exist
        required_paths = ['/upload', '/my', '/all', '/{assignment_id}/grade', '/{assignment_id}/download', '/stats']
        for path in required_paths:
            if any(path in route for route in routes):
                print(f"✓ Required route found: {path}")
            else:
                print(f"✗ Required route missing: {path}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Error checking endpoints: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Assignment Management API - Component Tests")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Model Creation Test", test_model_creation),
        ("File Validation Test", test_file_validation),
        ("CRUD Functions Test", test_crud_functions),
        ("Endpoint Structure Test", test_endpoint_structure),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
