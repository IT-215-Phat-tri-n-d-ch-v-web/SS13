from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

# Ràng buộc giá trị kích thước khoang
class RoomSizeEnum(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

# Ràng buộc giá trị trạng thái khoang
class StatusEnum(str, Enum):
    VACANT = "VACANT"
    OCCUPIED = "OCCUPIED"

class BoardingSlotBase(BaseModel):
    slot_number: str = Field(..., min_length=1, description="Mã số khoang chuồng không được để trống")
    room_size: RoomSizeEnum = Field(..., description="Kích thước phải là SMALL, MEDIUM, hoặc LARGE")
    price_per_day: float = Field(..., gt=0, description="Đơn giá thuê mỗi ngày phải là số lớn hơn 0")
    status: StatusEnum = Field(default=StatusEnum.VACANT)

class BoardingSlotCreate(BoardingSlotBase):
    pass

class BoardingSlotUpdate(BaseModel):
    slot_number: Optional[str] = Field(None, min_length=1)
    room_size: Optional[RoomSizeEnum] = None
    price_per_day: Optional[float] = Field(None, gt=0)
    status: Optional[StatusEnum] = None

class BoardingSlotResponse(BoardingSlotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)