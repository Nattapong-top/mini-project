import pytest
from datetime import datetime 
from domain.models import PricingPolicy

@pytest.fixture
def standard_policy():
    return PricingPolicy(
        hour_limit=24,
        free_hour=2,
        hourly_rate=20,
        max_daily=200,
        is_list=False
    )

@pytest.fixture
def fixed_now():
    return datetime.now()