from pydantic import BaseModel, Field


class MoneyThb(BaseModel):
    # เงินต้องไม่มีค่าเป็นลบ
    value: float = Field(ge=0, description='จำนวนเงินบาทไทย')

    def __add__(self, other):
        return MoneyThb(value=self.value + other.value)
    
    def __eq__(self, other):
        if isinstance(other, MoneyThb):
            return self.value == other.value
        if isinstance(other, (int, float)):
            return self.value == other
        return False
    
    # ทำให้เปรียบเทียบ มากกว่า/เท่ากับ ได้ เช่น MoneyThb(40) >= 20
    def __ge__(self, other):
        if isinstance(other, MoneyThb):
            return self.value >= other.value
        if isinstance(other, (int, float)):
            return self.value >= other
        return False

    # (แถม) เพื่อให้แสดงผลใน Log สวยๆ เวลา Test พัง
    def __repr__(self):
        return f"MoneyThb({self.value} THB)"

class LicensePlate(BaseModel):
    value: str = Field(..., min_length=1, max_length=10)
