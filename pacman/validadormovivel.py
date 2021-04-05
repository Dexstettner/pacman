from abc import ABCMeta, abstractmethod


class ValidadorMovivel(metaclass=ABCMeta):
    @abstractmethod
    def adicionar_movivel(self, movivel):
        pass
