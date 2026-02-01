import os
import pytest
from src.database.repository import VehicleRepository


@pytest.fixture
def repo(tmp_path):
    file = tmp_path / 'test_db.json'
    return VehicleRepository(str(file))


def test_save_and_load_data(repo):
    # Arrange: ข้อมูลสมมติของป๋า
    data = {'กข-1234': '2026-01-27 10:00:00', 'รถซิ่ง-007': '2026-01-27 11:00:00'}

    # Act: บันทึกและโหลด
    repo.save_all(data)
    loaded_data = repo.load_all()

    assert loaded_data == data
    assert loaded_data['กข-1234'] == '2026-01-27 10:00:00'

def test_load_empty_file_should_return_empty_dict(repo):
    assert repo.load_all() == {}

