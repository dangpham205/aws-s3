from fastapi import APIRouter, File, UploadFile


router = APIRouter(
    prefix="/workflow",
    tags=["Workflow"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(JWTBearer())],
)

@router.get('/')
async def root():
    return {'root': 'workflow'}