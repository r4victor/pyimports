import importlib.machinery
import importlib.util
import sys
import types


class NamespaceLoader(importlib.machinery.PathFinder):
    def __init__(self, namespace):
        self._namespace = namespace

    def find_spec(self, fullname, path=None, target=None):
        # Find the spec of the module using the default machinery
        spec = super().find_spec(fullname, path, target)
        
        # If the spec is found, modify its loader with our custom loader
        if spec:
            spec.loader = NamespaceAwareLoader(spec.loader, self._namespace)
        return spec


class NamespaceAwareLoader:
    def __init__(self, original_loader, namespace):
        self.original_loader = original_loader
        self.namespace = namespace

    def create_module(self, spec):
        return self.original_loader.create_module(spec)

    def exec_module(self, module):
        self.original_loader.exec_module(module)
        
        # This code doesn't make much sense since globals() will always refer
        # to the fancy2.py module dict. So during the import process we'll be
        # overriding globals()[self.namespace] until we assign the last one module,
        # which is the module we imported first.

        # After loading the module, assign it to the custom namespace
        if not hasattr(globals(), self.namespace):
            globals()[self.namespace] = types.SimpleNamespace()
        setattr(globals()[self.namespace], module.__name__, module)
        print(globals(), module.__name__)


def fancy_import_v2(module_name, namespace_name):
    # Use our custom loader
    loader = NamespaceLoader(namespace_name)
    
    # Insert our custom loader into the meta path
    sys.meta_path.insert(0, loader)
    
    # Try importing the module
    try:
        __import__(module_name)
    finally:
        # Ensure our loader is removed from the meta path
        sys.meta_path.remove(loader)

# Works
fancy_import_v2("mod1", "n1")

# Doesn't work since custom loader is not called.
# __import___ loads the module from sys.modules.
fancy_import_v2("mod1", "n2")
