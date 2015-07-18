import os
import shutil
import json
from gbdx_task_wrapper import TaskWrapper


class FileCountTask(TaskWrapper):
    __algo_output_file = "file_count.json"

    __directory_port_name = "directory"
    __recursive_port_name = "recursive"
    __output_data_port_name = "file_count_result"
    __output_string_port_name = "file_count"

    def __init__(self, work_path="/mnt/work/"):
        super(FileCountTask, self).__init__(work_path=work_path)

    def invoke(self):
        """
        Run the file count application
        """

        # Get inputs
        directory = self.get_input_data_port(self.__directory_port_name)
        recursive = self.get_input_string_port(self.__recursive_port_name, 'n')
        recursive = str(recursive).lower() in {'y', 'yes', 'true'}

        output_dir = self.get_output_data_port(self.__output_data_port_name)

        # Build and the command
        args = '{_dir}{_r}'.format(_dir=directory, _r='' if not recursive else ' -r')
        cmd = 'python /src/file_count/file_count.py' + ' ' + args
        print('Executing {_cmd}'.format(_cmd=cmd))
        os.system(cmd)

        if os.path.exists(self.__algo_output_file):
            with open(self.__algo_output_file, 'r') as f:
                self.__algo_output = json.load(f)
        else:
            print("Expected output missing.")
            return False

        # Copy output
        shutil.copy('file_count.json', output_dir)

        # Create output port
        self.set_output_string_port(self.__output_string_port_name, self.__algo_output['file_count'])

        print("Invoke complete")

        return True


if __name__ == "__main__":
    ret_val = False
    message = ""
    task_runner = None
    try:
        task_runner = FileCountTask()
        ret_val = task_runner.invoke()
    except Exception as e:
        print(str(e))
        message = str(e)
    finally:
        if task_runner:
            task_runner.finalize('success' if ret_val is True else 'failed', message)
