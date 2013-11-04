""" test project sanity """
import unittest

# Check project packages installed
from app.system import req_pkgs, pkg_mapping_module

class ProjectTestCase(unittest.TestCase):
    def runTest(self):
        for pkg in req_pkgs:
            if pkg_mapping_module.has_key(pkg):
                self.assertTrue(__import__(str(pkg_mapping_module[pkg])))
            else:
                self.assertTrue(__import__(str(pkg)))
