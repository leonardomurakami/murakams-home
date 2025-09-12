"""
Simple test runner script for development
Run with: python tests/test_runner.py
"""
import pytest
import sys
from pathlib import Path

def run_tests():
    """Run the test suite with appropriate configuration"""
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Basic test run arguments
    args = [
        "tests/",
        "-v",
        "--tb=short"
    ]
    
    # Add coverage if pytest-cov is available
    try:
        import pytest_cov
        args.extend([
            "--cov=app",
            "--cov-report=term-missing"
        ])
    except ImportError:
        print("pytest-cov not available, running without coverage")
    
    # Run tests
    exit_code = pytest.main(args)
    return exit_code

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
