import aiofiles
from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import Session
from typing_extensions import Annotated

from app.database.db import get_session
from app.repository.video import VideoRepository
from app.schemas.jwt import TokenData
from app.tools.jwt import credentials

router = APIRouter(prefix="/vids", tags=["videos"])


@router.post("/upload")
async def upload_video(
    video: UploadFile,
    session: Annotated[Session, Depends(get_session)],
    token_data: TokenData = Depends(credentials),
):

    out_file_path = f"uploads/{video.filename}"
    repository = VideoRepository(session=session)

    async with aiofiles.open(out_file_path, "wb") as out_file:
        content = await video.read()  # async read
        await out_file.write(content)  # async write

    assert video.filename is not None

    db_video = repository.create_video(
        title=video.filename,
        user_id=token_data.user_id,
        file_path=out_file_path,
    )

    return {
        "message": "Video uploaded successfully",
        "user": token_data.user_id,
        "filename": db_video.title,
    }
