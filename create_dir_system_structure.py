import os
from pathlib import Path

# กำหนดชื่อระบบ
system_name = 'parking_system'

def create_dir_system_structure():
    # กำหนดโครงสร้างโฟลเดอร์และไฟล์
    # key: โฟลเดอร์, value: รายการไฟล์ในโฟลเดอร์นั้น
    structure = {
        f'{system_name}': [
            "assets/",
            "data/",
            "docs/",
            "tests/",
            "requirements.txt",
            "README.md",
            "src/__init__.py",
            "src/main.py",
            "src/database/__init__.py",
            "src/database/db_manager.py",
            "src/logic/__init__.py",
            "src/logic/parking_lot.py",
            "src/logic/vehicle.py",
            "src/ui/__init__.py",
            "src/ui/entry_screen.py",
            "src/ui/exit_screen.py",
        ]
    }

    # สร้างโฟลเดอร์และไฟล์ตามโครงสร้างที่กำหนด
    for folder, files in structure.items():
        for file in files:
            path = Path(folder) / file

            if file.endswith('/'):
                # สร้างโฟลเดอร์
                path.mkdir(parents=True, exist_ok=True)
                print(f'Created directory: {path}')
            else:
                # สร้างโพลเดอร์ถ้ายังไม่มี
                path.parent.mkdir(parents=True, exist_ok=True)
                # สร้างไฟล์
                path.touch(exist_ok=True)
                print(f'Created file: {path}')

if __name__ == '__main__':
    create_dir_system_structure()
    print(f'Directory {system_name} structure created successfully.')