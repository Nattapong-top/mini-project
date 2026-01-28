import pytest
from src.database.sqlite_repository import SqliteRepository

@pytest.fixture
def repo(tmp_path):
    db_file = tmp_path / 'test_parking.db'
    return SqliteRepository(str(db_file))

def test_save_and_load(repo):
    # Arrange: ข้อมูลสมมติของป๋า
    data = {'กข-1234': '2026-01-27 10:00:00', 'รถซิ่ง-007': '2026-01-27 11:00:00'}

    # Act: วนลูปเพื่อบันทึกข้อมูลทีละคัน (ใช้ repo.save แทน create_tables)
    for license_plate, entry_time in data.items():
        repo.save_vehicle_in_parking(license_plate, entry_time)

    # Assert: โหลดข้อมูลกับมาเช็ค
    loaded_data = repo.show_all_vehicle_in_parking()

    assert loaded_data == data
    assert loaded_data['กข-1234'] == '2026-01-27 10:00:00'

def test_remove_vehicle(repo):
    license_plate = 'กข-9999'
    repo.save_vehicle_in_parking(license_plate, '2026-01-27 10:00:00')

    # Act: รถคันนี้ขับออกไป สั่งลบ
    repo.remove_vehicle_in_parking(license_plate)

    # Assert: ตรวจสอบว่าใน Datebase ต้องไม่เหลือรถคันนี้
    repo.show_all_vehicle_in_parking()
    assert license_plate

def test_check_vehicle_in_parking(repo):

    repo.save_vehicle_in_parking('รถซิ่ง-007', '2026-01-27 11:00:00')
    check_vehicle_in_parking = repo.check_vehicle_in_parking('รถซิ่ง-007')
    assert check_vehicle_in_parking == 'รถซิ่ง-007'

def test_connot_park_duplicate_license_plate(repo):
    license_plate = 'รถซิ่ง-007'
    repo.save_vehicle_in_parking(license_plate, '2026-01-27 11:00:00')
    existing_vehicle = repo.check_vehicle_in_parking(license_plate)
    assert existing_vehicle != None



