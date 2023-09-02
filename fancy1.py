import sys
import types


def fancy_import(module_name, namespace_name):
    # Back up the module from sys.modules if it exists
    cached_module = sys.modules.pop(module_name, None)
    
    # Use Python's __import__ function to import the module
    new_module = __import__(module_name)
    
    # Create a new namespace if it doesn't exist yet
    if namespace_name not in globals():
        globals()[namespace_name] = types.SimpleNamespace()
    
    # Assign the imported module to the namespace
    setattr(globals()[namespace_name], module_name, new_module)
    
    # Restore the module in sys.modules if it was there
    if cached_module:
        sys.modules[module_name] = cached_module

# Works
fancy_import("mod1", "n1")

# Works. But if we change mod2 (a transitive module),
# the change won't be reflected in n2 since it will be loaded from sys.modules.
fancy_import("mod1", "n2")
