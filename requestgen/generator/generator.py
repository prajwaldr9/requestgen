from abc import ABCMeta, abstractmethod


class Generator(metaclass=ABCMeta):
    def __init__(self):
        self.code = ''

    @abstractmethod
    def generate_code(self):
        pass

    def new_lines(self, n):
        return '\n' * n

    def add(self, code):
        self.code += code
