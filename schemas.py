from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    AVAILABLE = "AVAILABLE"
    OUT_OF_STOCK = "OUT_OF_STOCK"

class MenuItemBase(BaseModel):
    dish_code: str = Field(..., min_length=1, description="Mã món ăn không được rỗng")
    dish_name: str = Field(..., min_length=1, description="Tên món ăn không được rỗng")
    calorie_count: int = Field(..., gt=0, description="Hàm lượng calo phải lớn hơn 0")
    price: float = Field(..., gt=0, description="Đơn giá phải lớn hơn 0")
    status: StatusEnum = Field(default=StatusEnum.AVAILABLE)

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = Field(None, min_length=1)
    dish_name: Optional[str] = Field(None, min_length=1)
    calorie_count: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[StatusEnum] = None

class MenuItemResponse(MenuItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)