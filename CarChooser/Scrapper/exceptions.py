class AutoRiaException(Exception):
    # Class for exceptions of processing cars data from AutoRia website
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"Class called for error: {self.message}"
