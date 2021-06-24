import sys
from mrc_scripts.test_efs_backup import Test_backup

class TestQmi:

    def __init__(self, dev_id):

        self.dev_id = dev_id

    def test_qmi_tests(self):

        fin_out = qmi_obj.test_backup_main_method()
        print(fin_out)

#-------- Execution begins here ---------#
dev_id = sys.argv[1]

qmi_obj = Test_backup(dev_id)

