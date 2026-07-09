from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Any

import model2
from database2 import engine, get_db
import schemas2
import slot_service

# Đồng bộ cấu trúc bảng tự động khi khởi chạy ứng dụng
model2.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Hàm bổ trợ định dạng đúng cấu trúc 6 trường bắt buộc của đề bài
def create_standard_response(status_code: int, message: str, path: str, data: Any = None, error: str = None):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

@app.post("/boarding-slots")
def create_slot(slot_in: schemas2.BoardingSlotCreate, request: Request, db: Session = Depends(get_db)):
    # Ràng buộc kiểm tra tính duy nhất của mã số khoang chuồng
    existing = slot_service.get_boarding_slot_by_number(db, slot_number=slot_in.slot_number)
    if existing:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=create_standard_response(400, "Slot number already exists", request.url.path, error="Bad Request")
        )
    try:
        new_slot = slot_service.create_boarding_slot(db=db, slot=slot_in)
        data = schemas2.BoardingSlotResponse.model_validate(new_slot).model_dump()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=create_standard_response(201, "Thêm khoang lưu trú thành công", request.url.path, data=data)
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=create_standard_response(500, "Lỗi hệ thống database nội bộ", request.url.path, error=str(e))
        )

@app.get("/boarding-slots")
def read_slots(request: Request, db: Session = Depends(get_db)):
    slots = slot_service.get_boarding_slots(db)
    data = [schemas2.BoardingSlotResponse.model_validate(s).model_dump() for s in slots]
    return create_standard_response(200, "Lấy danh sách thành công", request.url.path, data=data)

@app.get("/boarding-slots/{slot_id}")
def read_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    db_slot = slot_service.get_boarding_slot(db, slot_id=slot_id)
    if db_slot is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=create_standard_response(404, "Boarding slot not found", request.url.path, error="Not Found")
        )
    data = schemas2.BoardingSlotResponse.model_validate(db_slot).model_dump()
    return create_standard_response(200, "Lấy chi tiết thành công", request.url.path, data=data)

@app.put("/boarding-slots/{slot_id}")
def update_slot(slot_id: int, slot_in: schemas2.BoardingSlotUpdate, request: Request, db: Session = Depends(get_db)):
    db_slot = slot_service.get_boarding_slot(db, slot_id=slot_id)
    if db_slot is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=create_standard_response(404, "Boarding slot not found", request.url.path, error="Not Found")
        )
    
    # Nếu cập nhật mã số khoang chuồng mới, bắt buộc đối soát tránh trùng lặp bản ghi khác
    if slot_in.slot_number and slot_in.slot_number != db_slot.slot_number:
        existing = slot_service.get_boarding_slot_by_number(db, slot_number=slot_in.slot_number)
        if existing:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=create_standard_response(400, "Slot number already exists", request.url.path, error="Bad Request")
            )

    try:
        updated_slot = slot_service.update_boarding_slot(db=db, db_slot=db_slot, slot_update=slot_in)
        data = schemas2.BoardingSlotResponse.model_validate(updated_slot).model_dump()
        return create_standard_response(200, "Cập nhật khoang lưu trú thành công", request.url.path, data=data)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=create_standard_response(500, "Lỗi cập nhật hệ thống", request.url.path, error=str(e))
        )

@app.delete("/boarding-slots/{slot_id}")
def delete_slot(slot_id: int, request: Request, db: Session = Depends(get_db)):
    db_slot = slot_service.get_boarding_slot(db, slot_id=slot_id)
    if db_slot is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=create_standard_response(404, "Boarding slot not found", request.url.path, error="Not Found")
        )
    try:
        slot_service.delete_boarding_slot(db=db, db_slot=db_slot)
        return create_standard_response(200, "Xóa khoang lưu trú thành công", request.url.path)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=create_standard_response(500, "Lỗi xóa dữ liệu hệ thống", request.url.path, error=str(e))
        )