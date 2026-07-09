from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Any

import model
from database import engine, get_db
import schemas
import menu_service

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def create_standard_response(status_code: int, message: str, path: str, data: Any = None, error: str = None):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

@app.post("/menu-items")
def create_item(item: schemas.MenuItemCreate, request: Request, db: Session = Depends(get_db)):
    # Kiểm tra trùng lặp dish_code
    existing = menu_service.get_menu_item_by_code(db, dish_code=item.dish_code)
    if existing:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=create_standard_response(400, "Mã món ăn đã tồn tại", request.url.path, error="Bad Request")
        )
    try:
        new_item = menu_service.create_menu_item(db=db, item=item)
        data = schemas.MenuItemResponse.model_validate(new_item).model_dump()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=create_standard_response(201, "Thêm món ăn thành công", request.url.path, data=data)
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=create_standard_response(500, "Lỗi máy chủ", request.url.path, error=str(e))
        )

@app.get("/menu-items")
def read_items(request: Request, db: Session = Depends(get_db)):
    items = menu_service.get_menu_items(db)
    data = [schemas.MenuItemResponse.model_validate(item).model_dump() for item in items]
    return create_standard_response(200, "Lấy danh sách món ăn thành công", request.url.path, data=data)

@app.get("/menu-items/{item_id}")
def read_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    db_item = menu_service.get_menu_item(db, item_id=item_id)
    if db_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=create_standard_response(404, "Menu item not found", request.url.path, error="Not Found")
        )
    data = schemas.MenuItemResponse.model_validate(db_item).model_dump()
    return create_standard_response(200, "Lấy thông tin chi tiết thành công", request.url.path, data=data)

@app.put("/menu-items/{item_id}")
def update_item(item_id: int, item: schemas.MenuItemUpdate, request: Request, db: Session = Depends(get_db)):
    db_item = menu_service.get_menu_item(db, item_id=item_id)
    if db_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=create_standard_response(404, "Menu item not found", request.url.path, error="Not Found")
        )
    
    if item.dish_code and item.dish_code != db_item.dish_code:
        existing = menu_service.get_menu_item_by_code(db, dish_code=item.dish_code)
        if existing:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=create_standard_response(400, "Mã món ăn đã tồn tại", request.url.path, error="Bad Request")
            )

    try:
        updated_item = menu_service.update_menu_item(db=db, db_item=db_item, item_update=item)
        data = schemas.MenuItemResponse.model_validate(updated_item).model_dump()
        return create_standard_response(200, "Cập nhật món ăn thành công", request.url.path, data=data)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=create_standard_response(500, "Lỗi máy chủ", request.url.path, error=str(e))
        )

@app.delete("/menu-items/{item_id}")
def delete_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    db_item = menu_service.get_menu_item(db, item_id=item_id)
    if db_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=create_standard_response(404, "Menu item not found", request.url.path, error="Not Found")
        )
    try:
        menu_service.delete_menu_item(db=db, db_item=db_item)
        return create_standard_response(200, "Xóa món ăn thành công", request.url.path)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=create_standard_response(500, "Lỗi máy chủ", request.url.path, error=str(e))
        )