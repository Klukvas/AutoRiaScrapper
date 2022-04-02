
class AutoRiaException(Exception):
    
    def name(self):
        return self.__class__.__name__