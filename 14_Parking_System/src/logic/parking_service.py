class ParkingService:
    def __init__(self, repo):
        self.repo = repo

    def register_vehicle_entry(self, license_plate, entry_time):
        existing = self.repo.check_vehicle_in_parking(license_plate)
    
        if existing:
            return f'Error: ทะเบียนซ้ำรถ {license_plate} จอดอยู่แล้ว'
        
        self.repo.save_vehicle_in_parking(license_plate, entry_time)
        return 'Success: จอดเรียบร้อย!'
    
    def register_vehicle_exit(self, license_plate):
        existing = self.repo.check_vehicle_in_parking(license_plate)

        if not existing:
            return f'Error: ไม่พบทะเบียน {license_plate}'
        
        self.repo.save_vehicle_in_parking(license_plate)
        return f'Success: รถทะเบียน {license_plate} ออกเรียบร้อย!'
    
    # def count_all_vehicle_in_parking(self):
    #     self.repo.