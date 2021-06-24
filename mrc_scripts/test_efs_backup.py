import time
import os
import sys
import subprocess
from pathlib import Path

class Test_backup:

    def __init__(self, dev_id):

        self.dev_id = dev_id
        self.previous_count = 0

        # Shell script path
        current_dir = Path(__file__).parent.absolute()
        self.shell_script_path = str(current_dir).replace('\\', '/') + '/shell_scripts/'

        # Test result Output directory
        self.log_path = str(current_dir) + "\\" + 'shell_scripts'

    def test_backup_main_method(self):

        try:
            os.system('rm -rf ' + self.log_path + 'log_1.txt')
        except:
            pass

        print("Test Case - Backup")
        os.system('adb -s ' + dev_id + ' wait-for-device')
        outfile = open(self.shell_script_path + '\log_1.txt', 'w')
        proc_id = subprocess.Popen(
            'sh ' + '"' + self.shell_script_path + '"' + '/backup_app_start.sh ' + self.dev_id, stdout=outfile,
            stderr=subprocess.DEVNULL)


        for iteration in range(1,2):

            return_value = backup_obj.test_method_backup(iteration)
            if return_value == "fail":
                break

        #Terminating the subprocess created to clear the memory
        proc_id.terminate()

        return return_value

    def test_method_backup(self, iteration):

        # Enter the backup timer interval in below sleep command
        sleep_time = 450
        print("*" * 50)
        print("Iteration " + str(iteration) + ":- Waiting for " + str(sleep_time) + " seconds for backup process to complete")
        print("*" * 50)
        time.sleep(sleep_time)

        return_value = backup_obj.test_check_backup_results()
        return return_value

    #This function checks whether the backup file size is proper.
    def test_check_backup_results(self):

        backup_sucess_count = 0
        file = open(self.shell_script_path + "log_1.txt", "r")

        for line in file:

            line = line.strip()  # Removing all the un-necessary spaces in the line.
            keyword_search = line.split()  # Spiliting the line wrt space, so that it will be converted to a list of words.

            for word_search in keyword_search:  # This loop will go through word by word in one single line.

                if "complete" in word_search:  # Checking whether that line contains restore! word

                    backup_sucess_count = backup_sucess_count + 1
                    break  # Stepping out of this loop once. But eventually, for loop will go through each line.

        file.close()

        if backup_sucess_count > self.previous_count:
            self.previous_count = backup_sucess_count
            return_value = backup_obj.test_backup_file_size_check()
            return return_value

        else:
            print("Backup failed. Backup count is :- ", backup_sucess_count)
            print("Previous Backup count is :- ", self.previous_count)
            self.previous_count = backup_sucess_count
            return "fail"

    def test_backup_file_size_check(self):

        try:
            os.system('rm -rf ' + self.shell_script_path + '\\backup_file_details.txt')
        except:
            pass

        time.sleep(3)
        outfile = open(self.shell_script_path + '\\backup_file_details.txt', 'w')

        proc_id = subprocess.Popen(
            'adb -s '+ self.dev_id + ' shell ls -al /data/efsbackup/runtime/', stdout=outfile,
            stderr=subprocess.DEVNULL)

        time.sleep(5)
        proc_id.terminate()

        file = open(self.shell_script_path + "backup_file_details.txt", "r")

        for line in file:  # This loop will go through each line in the log file, one by one.
            line = line.strip()  # Removing all the un-necessary spaces in the line.
            keyword_search = line.split()  # Spiliting the line wrt space, so that it will be converted to a list of words.

            for word_search in keyword_search:  # This loop will go through word by word in one single line.

                backup_names = ["bkpcpy-03.bin", "bkpcpy-02.bin", "bkpcpy-01.bin"]
                for file_names in backup_names:

                    if file_names in word_search:

                        backup_size = keyword_search[-5]

                        if backup_size == 0:
                            print("Failing the test case as file size of " + file_names + " is :- ", backup_size)
                            backup_size_flag = 0

                        else:
                            #print("Size of the " + file_names + " file is proper :- ", backup_size)
                            backup_size_flag = 1


        if backup_size_flag == 1:
            print("*** Pass ***")
            return "pass"
        else:
            print("*** Fail ***")
            return "fail"


dev_id = sys.argv[1]
backup_obj = Test_backup(dev_id)

if __name__ == "__main__":

    backup_obj.test_backup_main_method()
