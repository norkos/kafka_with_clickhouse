from fastapi import APIRouter

router = APIRouter(
    prefix='/api'
)

@router.post("/event")
async def event():
    return {"message": "Hello World"}

@router.get("/report")
async def report():
    return {"message": "Hello World"}
