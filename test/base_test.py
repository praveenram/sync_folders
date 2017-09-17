from unittest import TestCase
import os, uuid

class BaseTest(TestCase):
    def setup(self):
        self.tmpDir = '/tmp/tmp-%s' % (uuid.uuid4().hex)
        os.makedirs(self.tmpDir)

    def teardown(self):
        os.removedirs(self.tmpDir)
