import glob
import os

from app.system.log import logger as _slk

def _import_test(basename, name):
    try:
        module = __import__('%s' % (basename,), globals(), locals(), fromlist=[name])
    except ImportError:
        return None
    return getattr(module, name)

def discover_tests(path):
    tests = list()
    for name in glob.glob(os.path.join(path,'*.py')):
        name = os.path.basename(name)[:-3]
        if '__' not in name:
            module_name = name.lower()
            class_name = name.capitalize()
            class_name_full = "%sTestCase" % (class_name,)
            _slk.debug("Searching class %s" % (class_name_full,))
            test_base = _import_test("app.system.tests.%s" % (name,), class_name_full)
            _slk.debug("Imported: %s/%s" % (name, test_base,))
            tests.append(test_base())
    return tests
