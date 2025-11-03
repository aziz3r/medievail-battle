from abc import ABC, abstractmethod
import string

class General(ABC):
    def __init__(self, nom: string = None):
        self.nom = nom

    """à implémenter plus tard selon le général"""
    @abstractmethod
    def strategie(self):  
        pass