import imax
# import resource_counter as rc
import sys
import importlib.util

file_path = '../resource_counter/action/scripting_test.py'
module_name = 'scripting_test'

spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.modules[module_name] = module

from scripting_test import testing_method, testing_value

imax.print('runtime imported method: ', testing_method())
imax.print('runtime imported value: ', testing_value)
