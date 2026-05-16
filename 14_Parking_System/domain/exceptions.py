# domain/exceptions.py

class OverLimitError(Exception):
    """Exception สำหรับกรณีจอดรถเกินเวลาที่กำหนด"""
    pass

class InsufficientPaymentError(Exception):
    """Exception สำหรับกรณีจ่ายเงินไม่ครบ"""
    pass

class ConcurrencyError(Exception):
    '''Exception คนอื่นแก้ไขข้อมูลไปแล้ว'''