from fastapi import FastAPI, APIRouter,  HTTPException, status, Depends, File, UploadFile


router = APIRouter()


@router.post("/chat")
async def chat(question: str):
    pass
