from fastapi import APIRouter
from fastapiprojecti.api.v1.endpoints.kc_router import router as kc_router


router = APIRouter(prefix="/api/v1", tags=["v1"])

router.include_router(kc_router)


@router.get("/health")
async def health():
    return {"status": "ok"}