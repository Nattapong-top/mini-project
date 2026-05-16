from abc import ABC, abstractmethod

class BarrierInterface(ABC):
    @abstractmethod
    def open(self) -> None:
        '''สั่งไม่กั้นยกขึ้'''
        pass

    @abstractmethod
    def close(self) -> None:
        '''สั่งไม้กั้นยกลง'''
        pass