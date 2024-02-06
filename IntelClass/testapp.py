from abc import ABC, abstractmethod

class A(ABC):
    @abstractmethod
    def move(self):
        pass

a = A()
a.move() 