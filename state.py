class State(object):

    def __init__(self, numbers, df=None):
        self._numbers = numbers
        self._data_frame = df
        print('Processing current state: ', str(self))

    def get_numbers(self):
        return self._numbers
    
    def set_numbers(self, value):
        self._numbers = value

    def get_data_frame(self):
        return self._data_frame
    
    def set_data_frame(self, value):
        self._data_frame = value

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return self.__class__.__name__
    
    def next(self):
        pass

    def gera(self, numbers):
        pass

    