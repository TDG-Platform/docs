import os
import json


class TaskWrapper(object):
    """A job runner base class.
    """

    def __init__(self, work_path="/mnt/work/"):
        self.__work_path = work_path
        self.__string_input_ports = None

        if not os.path.exists(self.__work_path):
            raise Exception("Working path must exist. {_path}.".format(_path=self.__work_path))

        string_input_ports = os.path.join(self.__work_path, 'input', "ports.json")
        if os.path.exists(string_input_ports):
            with open(string_input_ports, 'r') as f:
                self.__string_input_ports = json.load(f)

    @property
    def base_path(self):
        return self.__work_path

    @property
    def input_path(self):
        return os.path.join(self.base_path, 'input')

    @property
    def output_path(self):
        return os.path.join(self.base_path, 'output')

    def get_input_string_port(self, port_name, default=None):
        """
        Get input string port value
        :param port_name:
        :param default:
        :return: :rtype:
        """
        if self.__string_input_ports:
            return self.__string_input_ports.get(port_name, default)
        return default

    def get_input_data_port(self, port_name):
        """
        Get the input location for a specific port
        :param port_name:
        :return: :rtype:
        """
        return os.path.join(self.input_path, port_name)

    def get_output_data_port(self, port_name):
        """
        Get the output location for a specific port
        :param port_name:
        :return: :rtype:
        """
        return os.path.join(self.output_path, port_name)

    def invoke(self):
        """
        The do something method
        :rtype : bool
        :raise RuntimeError:
        """
        raise RuntimeError("JobRunner Baseclass invoke is not callable")

    def finalize(self, success_or_fail, message):
        """
        :param success_or_fail: string that is 'success' or 'fail'
        :param message:
        """
        with open(os.path.join(self.base_path, 'status.json'), 'w') as f:
            json.dump({'status': success_or_fail, 'reason': message}, f, indent=4)
