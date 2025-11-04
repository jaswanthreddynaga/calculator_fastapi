# app/operations/__init__.py

"""
Operations module initialization.

This module exports all arithmetic operations from the parent app.operations module
for convenient importing.
"""

# Import from the parent app directory's operations.py file
# We need to import from the parent module (app) and then access operations
import sys
import os

# Get the app directory
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Import operations module from parent directory
import importlib.util
operations_path = os.path.join(app_dir, 'operations.py')
spec = importlib.util.spec_from_file_location("app.operations_module", operations_path)
operations_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operations_module)

# Re-export the functions
add = operations_module.add
subtract = operations_module.subtract
multiply = operations_module.multiply
divide = operations_module.divide

__all__ = ['add', 'subtract', 'multiply', 'divide']
