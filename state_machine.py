from number_generator_states import *


class StateMachine(object):

    def __init__(self):
        """
        Inicializa os componentes
        """
        self._numbers = []
        self.state = Comeca(numbers=self.get_numbers())

    def get_numbers(self):
        return self._numbers
    
    def set_numbers(self, value):
        self._numbers = value

    def next(self):
        self.state = self.state.next()