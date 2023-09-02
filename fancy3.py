import sys
import types


def fancy_import_v3(module_name, namespace_name):
    # Save sys.modules so that we can restore it after importing.
    # Since importing doesn't affect sys.modules, transitive modules are reloaded.
    saved_sys_modules = sys.modules.copy()
    
    try:
        # Use Python's __import__ function to import the module
        new_module = __import__(module_name)

        # Create a new namespace
        globals()[namespace_name] = types.SimpleNamespace()

        # Assign the imported module to the namespace
        # TODO: make it work with nested imports e.g. "a.b.c"
        setattr(globals()[namespace_name], module_name, new_module)
    finally:
        # We have to change sys.modules vs just reassigning it because python's
        # import machinery accesses it via PyThreadState_GET()->interp->modules
        sys.modules.clear()
        for mod_name, mod in saved_sys_modules.items():
            sys.modules[mod_name] = mod


fancy_import_v3("mod1", "n1")

# Update mod1/mod2 and see that n1 and n2 are different

fancy_import_v3("mod1", "n2")

# The approach should work correctly for reloading Python modules,
# but may not work for C extensions which are tied to the interpreter state.
# Once a shared library is loaded, it won't be reloaded.
