from adapters.repository_interface import ParkingRepository
from domain.models import ParkingTicket, LicensePlate

class InMemoryParkingRepository(ParkingRepository):
    def __init__(self):
        # ใช้ Dictionary เป็นตัวเก็บข้อมูล (เหมือน Database จำลอง)
        # key คือ เลขทะเบียน, value คือ Object ของ ParkingTicket
        self._db = {}

    def save(self, ticket: ParkingTicket):
        # บันทึกลง RAM
        self._db[ticket.license_plate.value] = ticket

    def get_by_plate(self, plate: LicensePlate):
        # ดึงจาก RAM
        return self._db.get(plate.value)