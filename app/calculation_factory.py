from abc import ABC, abstractmethod

class Operation(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass

class Add(Operation):
    def execute(self, a, b):
        return a + b

class Subtract(Operation):
    def execute(self, a, b):
        return a - b

class Multiply(Operation):
    def execute(self, a, b):
        return a * b

class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class CalculationFactory:
    @staticmethod
    def create_operation(type: str) -> Operation:
        if type == "Add":
            return Add()
        elif type == "Subtract":
            return Subtract()
        elif type == "Multiply":
            return Multiply()
        elif type == "Divide":
            return Divide()
        else:
            raise ValueError(f"Unknown operation type: {type}")
