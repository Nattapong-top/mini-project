import json
import os

class VehicleRepository:
    '''Adapter สำหรับจัดการการเก็บข้อมูลรถลงไฟล์ JSON'''
    def __init__(self, file_path = '/14_Parking_System/data/parking_data.json'):
        self.file_path = file_path

    def save_all(self, parked_vehicles):
        '''บันทึก dictionary ทั้งหมดลงไฟล์'''
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(parked_vehicles, f, ensure_ascii=False, indent=4)
    
    def load_all(self):
        '''โหลดข้อมูลทั้งหมดขึ้นมา'''
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
        
