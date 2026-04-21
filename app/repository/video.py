from sqlmodel import Session, select

from app.models.videos import Video, VideoQuality


class VideoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_video_by_id(self, video_id: int):
        statement = select(Video).where(Video.id == video_id)
        result = self.session.exec(statement).first()
        return result

    def get_video_by_id_and_user_id(self, video_id: int, user_id: int):
        statement = select(Video).where(Video.id == video_id, Video.user_id == user_id)
        result = self.session.exec(statement).first()
        return result

    def create_video(self, title: str, user_id: int, file_path: str):
        new_video = Video(
            title=title,
            user_id=user_id,
            file=file_path,
        )
        self.session.add(new_video)
        self.session.commit()
        self.session.refresh(new_video)
        return new_video

    def get_videos_by_user_id(self, user_id: int):
        statement = select(Video).where(Video.user_id == user_id)
        result = self.session.exec(statement).all()
        return result

    def get_video_qualities(self, video_id: int):
        statement = select(VideoQuality).where(VideoQuality.video_id == video_id)
        result = self.session.exec(statement).all()
        return result