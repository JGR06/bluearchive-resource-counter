import sys
import importlib.util


root_path = '../resource_counter'


# runtime import specific script
# as example, filename is 'action/scripting_test.py' and module_name is 'scripting_test'
# call this function before use other module
def import_specific_module(filename, module_name):
    file_path = f'{root_path}/{filename}'

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[module_name] = module
