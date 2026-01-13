#!/usr/bin/env python3
"""
Verification script to check if all dependencies are properly installed
and the project structure is correct.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_dependencies():
    """Check if all required Python packages are available."""
    print("Checking Python dependencies...")
    
    required_packages = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("sqlalchemy", "Database toolkit"),
        ("pydantic", "Data validation library"),
        ("jwt", "JSON Web Token implementation"),  # pyjwt imports as jwt
        ("passlib", "Password hashing library"),
        ("alembic", "Database migration tool"),
        ("psycopg2", "PostgreSQL adapter"),
        ("python_dateutil", "Date utilities"),
        ("cryptography", "Cryptographic recipes"),
    ]
    
    missing_packages = []
    for package, description in required_packages:
        try:
            __import__(package.replace("-", "_").replace("python_", ""))
            print(f"  ✓ {package} - {description}")
        except ImportError:
            missing_packages.append((package, description))
            print(f"  ✗ {package} - {description}")
    
    if missing_packages:
        print(f"\nFound {len(missing_packages)} missing Python packages.")
        return False
    
    return True

def check_node_dependencies():
    """Check if Node.js and npm are available."""
    print("\nChecking Node.js dependencies...")
    
    try:
        node_version = subprocess.check_output(["node", "--version"], text=True).strip()
        print(f"  ✓ Node.js {node_version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ✗ Node.js not found")
        return False
    
    try:
        npm_version = subprocess.check_output(["npm", "--version"], text=True).strip()
        print(f"  ✓ npm {npm_version}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ✗ npm not found")
        return False
    
    return True

def check_project_structure():
    """Check if essential project files and directories exist."""
    print("\nChecking project structure...")
    
    essential_paths = [
        ("src", "Source code directory"),
        ("src/backend-python", "Python backend directory"),
        ("src/frontend", "Frontend directory"),
        ("requirements.txt", "Python dependencies"),
        ("package.json", "Node.js dependencies"),
        ("main.py", "Main Python entry point"),
        ("electron-main.js", "Electron main process"),
    ]
    
    missing_paths = []
    for path, description in essential_paths:
        if Path(path).exists():
            print(f"  ✓ {path} - {description}")
        else:
            print(f"  ✗ {path} - {description}")
            missing_paths.append((path, description))
    
    if missing_paths:
        print(f"\nFound {len(missing_paths)} missing essential paths.")
        return False
    
    return True

def check_vendor_directory():
    """Check if vendor directory with pre-downloaded packages exists."""
    print("\nChecking vendor directory...")
    
    vendor_checks = [
        ("vendor", "Vendor directory"),
        ("vendor/node_modules", "Pre-downloaded Node.js packages"),
        ("vendor/python_packages", "Pre-downloaded Python packages"),
        ("install-vendor-deps.sh", "Vendor installation script"),
        ("VENDOR_INSTALLATION.md", "Vendor installation documentation"),
    ]
    
    vendor_exists = True
    for path, description in vendor_checks:
        if Path(path).exists():
            print(f"  ✓ {path} - {description}")
        else:
            print(f"  ⚠ {path} - {description} (optional)")
            if path in ["vendor", "vendor/node_modules", "vendor/python_packages"]:
                vendor_exists = False
    
    return vendor_exists

def main():
    """Run all checks and report results."""
    print("=" * 60)
    print("STRODSERVICE PROJECT VERIFICATION SCRIPT")
    print("=" * 60)
    
    checks = [
        ("Python Dependencies", check_python_dependencies),
        ("Node.js Dependencies", check_node_dependencies),
        ("Project Structure", check_project_structure),
        ("Vendor Directory", check_vendor_directory),
    ]
    
    results = {}
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * len(check_name))
        results[check_name] = check_func()
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY:")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        icon = "✓" if result else "✗"
        print(f"{icon} {check_name}: {status}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All checks passed! The project is ready for use.")
        print("\nTo start the application, you can:")
        print("  1. Run backend: python main.py backend")
        print("  2. Install vendor deps: npm run install-vendor")
        print("  3. Build release: ./build-release.sh (Linux/Mac) or double-click build-release.bat (Windows)")
    else:
        print("❌ Some checks failed. Please review the output above and fix issues before proceeding.")
        print("\nFor quick dependency installation from vendor:")
        print("  bash install-vendor-deps.sh")
        print("Or:")
        print("  npm run install-vendor")
        
    print("\n" + "=" * 60)
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())