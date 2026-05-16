from domain.barrier_interfaces import BarrierInterface
class BarrierSpy(BarrierInterface):
    def __init__(self):
        self.is_open = False    # สร้างสถานะ ไว้เช็คเองในตัวปลอม

    def open(self) -> None:
        self.is_open = True     # สั่งเปิดต้องเปลี่ยนเป็น True
    
    def close(self):
        self.is_open = False    
