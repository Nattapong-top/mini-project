from abc import ABC, abstractmethod
from domain.models import ParkingTicket, LicensePlate

class ParkingRepository(ABC):
    @abstractmethod
    def save(self, ticket: ParkingTicket):
        pass

    @abstractmethod
    def get_by_plate(self, plate: LicensePlate):
        pass

    