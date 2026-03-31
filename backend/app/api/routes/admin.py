from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user, get_db
from app.core.config import settings
from app.core.security import create_admin_token
from app.models.rewrite_record import RewriteRecord
from app.models.user import User

router = APIRouter()


# ——— 登录 ———

@router.post("/login")
def admin_login(body: dict):
    password = body.get("password", "")
    if password != settings.admin_password or not settings.admin_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="管理员密码错误",
        )
    token = create_admin_token()
    return {"access_token": token, "token_type": "bearer"}


# ——— 用户列表 ———

@router.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: str = Depends(get_admin_user),
):
    total = db.query(func.count(User.id)).scalar()
    users = (
        db.query(User)
        .order_by(User.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
    }


# ——— 改写记录列表 ———

@router.get("/records")
def list_records(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: str = Depends(get_admin_user),
):
    total = db.query(func.count(RewriteRecord.id)).scalar()
    records = (
        db.query(RewriteRecord)
        .order_by(RewriteRecord.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": r.id,
                "user_id": r.user_id,
                "username": r.user.username if r.user else "—",
                "source_preview": r.source_text[:80] + ("…" if len(r.source_text) > 80 else ""),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ],
    }


# ——— 删除用户 ———

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_admin_user),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    return {"message": f"用户 {user_id} 已删除"}


# ——— 删除记录 ———

@router.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_admin_user),
):
    record = db.get(RewriteRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(record)
    db.commit()
    return {"message": f"记录 {record_id} 已删除"}
