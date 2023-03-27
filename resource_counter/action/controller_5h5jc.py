import sys
import importlib.util

# TODO: fix dirty import
file_path = '../resource_counter/util.py'
module_name = 'util'

spec = importlib.util.spec_from_file_location(module_name, file_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.modules[module_name] = module

import util
util.import_specific_module('resource_counter.py', 'resource_counter')
import resource_counter
import imax


rc = resource_counter.ResourceCounter()
rc.run()


