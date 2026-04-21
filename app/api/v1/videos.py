import aiofiles
from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile
from sqlmodel import Session
from typing_extensions import Annotated

from app.core import exceptions
from app.database.db import get_session
from app.repository.video import VideoRepository
from app.schemas.jwt import TokenData
from app.schemas.videos import Video
from app.tasks.video_qualities_task import process_all_video_qualities
from app.tools.jwt import credentials

router = APIRouter(prefix="/vids", tags=["videos"])


@router.post("/upload")
async def upload_video(
    video: UploadFile,
    background_tasks: BackgroundTasks,
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
    background_tasks.add_task(
        func=process_all_video_qualities,
        video=db_video,
        session=session,
    )
    return {
        "message": "Video uploaded successfully",
        "user": token_data.user_id,
        "filename": db_video.title,
    }


@router.get("")
async def get_videos(
    session: Annotated[Session, Depends(get_session)],
    token_data: TokenData = Depends(credentials),
) -> list[Video]:
    repository = VideoRepository(session=session)
    videos = repository.get_videos_by_user_id(user_id=token_data.user_id)
    return videos


@router.get("/{video_id}")
async def get_video(
    video_id: int,
    session: Annotated[Session, Depends(get_session)],
    token_data: TokenData = Depends(credentials),
) -> Video:
    repository = VideoRepository(session=session)
    video = repository.get_video_by_id_and_user_id(
        video_id=video_id,
        user_id=token_data.user_id,
    )
    if not video:
        raise exceptions.ResourceNotFound

    return video
