#!/usr/bin/env python3
"""
Test script to verify that all important modules can be imported correctly
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing imports...")

# Test doc tracking system
try:
    from doc_tracking_system import DocTrackingSystem
    print("✓ doc_tracking_system imported successfully")
except Exception as e:
    print(f"✗ Failed to import doc_tracking_system: {e}")

# Test main functions
try:
    from main import start_doc_tracking_system, start_full_project, start_backend
    print("✓ main module functions imported successfully")
except Exception as e:
    print(f"✗ Failed to import main functions: {e}")

# Test backend imports
backend_path = project_root / "src" / "backend-python"
sys.path.insert(0, str(backend_path))

try:
    import app.models
    import app.schemas
    import app.crud
    print("✓ Backend modules imported successfully")
except Exception as e:
    print(f"✗ Failed to import backend modules: {e}")

# Test config
try:
    import config
    print("✓ config module imported successfully")
except Exception as e:
    print(f"✗ Failed to import config: {e}")

print("\nImport tests completed!")