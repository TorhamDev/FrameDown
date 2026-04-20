import subprocess

from sqlmodel import Session

from app.models.videos import Video, VideoQuality


def process_all_video_qualities(video: Video, session: Session):

    get_quality_command = "ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0"
    ffmpeg_commands = {
        "1080": '-vf "scale=1920:1080:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos" '
        "-c:v libx264 -preset slow -crf 22 -c:a aac -b:a 192k",
        "720": '-vf "scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos" '
        "-c:v libx264 -preset slow -crf 23 -c:a aac -b:a 128k",
        "480": '-vf "scale=854:480:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos" '
        "-c:v libx264 -preset slow -crf 23 -c:a aac -b:a 96k",
        "360": '-vf "scale=640:360:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos" '
        "-c:v libx264 -preset slow -crf 25 -c:a aac -b:a 64k",
        "240": '-vf "scale=426:240:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos" '
        "-c:v libx264 -preset slow -crf 27 -c:a aac -b:a 48k",
    }

    quality = (
        subprocess.check_output(f"{get_quality_command} {video.file}", shell=True)
        .decode()
        .strip()
    )

    for q, ffmpeg_command in ffmpeg_commands.items():
        print(quality, "+<<<<<<<")
        if int(quality.split(",")[1]) >= int(q):
            output_file = f"{video.file.rsplit('.', 1)[0]}_{q}p.mp4"
            command = f"ffmpeg -i {video.file} {ffmpeg_command} {output_file}"
            subprocess.run(command, shell=True, check=True)

            video_quality = VideoQuality(
                quality=q,
                file=output_file,
                video_id=video.id,
            )

            session.add(video_quality)

    session.commit()
