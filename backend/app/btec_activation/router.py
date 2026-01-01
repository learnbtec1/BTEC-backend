import uuid

from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from app.api.deps import CurrentUser, SessionDep
from app.btec_activation.schemas import (
    ActivateRequest,
    ActivationCreate,
    ActivationResponse,
)
from app.btec_activation.services import (
    consume_activation_token,
    create_activation_token,
    store_activation_key,
    verify_token,
)

router = APIRouter(prefix="/activation", tags=["activation"])


@router.post("/admin/generate", response_model=ActivationResponse)
async def admin_generate_key(
    payload: ActivationCreate,
    _background: BackgroundTasks,
    session: SessionDep,
    _current_user: CurrentUser
) -> ActivationResponse:
    """
    Generate activation key (Admin only).

    TODO: Add proper admin permission check based on project's auth system.
    """
    # TODO: Implement admin permission check
    # For now, any authenticated user can generate keys
    # In production, add: if not _current_user.is_superuser: raise HTTPException(403)

    jti = str(uuid.uuid4())
    token, expires_at = create_activation_token(
        jti,
        payload.student_id,
        payload.student_email,
        payload.specialization or "",
        payload.level or "",
        payload.validity_days
    )
    await store_activation_key(
        session,
        jti,
        payload.student_id,
        payload.student_email,
        payload.specialization,
        payload.level,
        expires_at
    )
    # TODO: Send email notification to student
    # _background.add_task(send_activation_email, payload.student_email, token)

    return ActivationResponse(token=token, jti=jti, expires_at=expires_at)


@router.post("/activate")
async def activate(
    req: ActivateRequest,
    request: Request,
    session: SessionDep
) -> dict:
    """
    Activate a student account using activation token.
    """
    try:
        payload = verify_token(req.token)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="رمز تفعيل غير صالح أو منتهي الصلاحية"
        )

    jti = payload.get("jti")
    key = await consume_activation_token(
        session,
        jti,
        used_ip=request.client.host if request.client else None
    )

    if not key:
        raise HTTPException(status_code=404, detail="مفتاح التفعيل غير موجود")

    if key.is_revoked or not key.is_active:
        raise HTTPException(status_code=403, detail="المفتاح موقوف أو ملغى")

    # TODO: Link activation key to actual student account in the system

    return {
        "status": "activated",
        "jti": jti,
        "student_id": key.student_id
    }
