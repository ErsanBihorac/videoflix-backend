import os
import shutil
import subprocess
import glob
from PIL import Image
from moviepy.editor import VideoFileClip

def convert_video_for_HLS_player(source, video_id, thumbnail_source):
    create_video_preview(source, video_id)
    comprimize_resize_thumbnail(thumbnail_source, video_id)
    create_master_playlist(source)
    convert_HLS_to_1080p(source)
    convert_HLS_to_720p(source)
    convert_HLS_to_480p(source)
    move_video_files(source, video_id)

def create_video_preview(source, video_id):
    source = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_directory = os.path.join('media', 'previews', str(video_id))

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    preview_file_path = os.path.join(target_directory, f'preview.mp4')

    with VideoFileClip(source) as video:
        preview = video.subclip(0, 3)
        preview.write_videofile(preview_file_path, codec='libx264', audio_codec='aac', fps=24)

def comprimize_resize_thumbnail(source, video_id):
    source = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_directory = os.path.join('media', 'thumbnails', str(video_id))

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    thumbnail_file_path = os.path.join(target_directory, f'thumbnail.jpeg')

    with Image.open(source) as img:
        img = img.convert('RGB')
        img.resize((120, 214))
        img.save(source, format='JPEG', quality=85, optimize=True) 

    shutil.move(source, thumbnail_file_path)

def move_video_files(source, video_id):
    source = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    base_name, _ = os.path.splitext(source)
    directory_linux, _ = os.path.split(source)
    target_directory = os.path.join('media', 'videos', str(video_id))

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    files_to_move = [
        f"{directory_linux}/master.m3u8",
        f"{base_name}.mp4",
        f"{base_name}_1080p.m3u8",
        f"{base_name}_720p.m3u8",
        f"{base_name}_480p.m3u8"
    ]

    for quality in ['1080p', '720p', '480p']:
        segment_pattern = f"{base_name}_{quality}_*.ts"
        segment_files = glob.glob(segment_pattern)
        files_to_move.extend(segment_files)

    for file_path in files_to_move:
        if os.path.exists(file_path):
            target_path = os.path.join(target_directory, os.path.basename(file_path))
            shutil.move(file_path, target_path)
        else:
            print(f"Datei nicht gefunden: {file_path}")

def create_master_playlist(source):
    file_name, _ = os.path.splitext(source)
    file_name_no_url = source.split('\\')[-1].split('.')[0]

    master_playlist_path = source.rsplit("\\", 1)[0] + "\\" + 'master.m3u8'
    master_playlist_path_linux = "/mnt/" + master_playlist_path.replace("\\", "/").replace("C:", "c")    

    with open(master_playlist_path_linux, 'w') as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080\n")
        f.write(f"{file_name_no_url}_1080p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720\n")
        f.write(f"{file_name_no_url}_720p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=1000000,RESOLUTION=854x480\n")
        f.write(f"{file_name_no_url}_480p.m3u8\n")

def convert_HLS_to_1080p(source):
    file_name, _ = os.path.splitext(source)
    target = file_name + '_1080p.m3u8'
    segment_filename = file_name + '_1080p_%03d.ts'

    source_linux = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_linux = "/mnt/" + target.replace("\\", "/").replace("C:", "c")
    segment_filename_linux = "/mnt/" + segment_filename.replace("\\", "/").replace("C:", "c")

    cmd = 'ffmpeg -i "{}" -vf scale=-2:1080 -c:v h264 -b:v 5000k -c:a aac -b:a 128k -hls_time 6 -hls_playlist_type vod -hls_segment_filename "{}" "{}"'.format(source_linux,segment_filename_linux, target_linux)
    subprocess.run(cmd, capture_output=True, shell=True)

def convert_HLS_to_720p(source):
    file_name, _ = os.path.splitext(source)
    target = file_name + '_720p.m3u8'
    segment_filename = file_name + '_720p_%03d.ts'

    source_linux = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_linux = "/mnt/" + target.replace("\\", "/").replace("C:", "c")
    segment_filename_linux = "/mnt/" + segment_filename.replace("\\", "/").replace("C:", "c")

    cmd = 'ffmpeg -i "{}" -vf scale=-2:720 -c:v h264 -b:v 3000k -c:a aac -b:a 128k -hls_time 6 -hls_playlist_type vod -hls_segment_filename "{}" "{}"'.format(source_linux,segment_filename_linux, target_linux)
    subprocess.run(cmd, capture_output=True, shell=True)

def convert_HLS_to_480p(source):
    file_name, _ = os.path.splitext(source)
    target = file_name + '_480p.m3u8'
    segment_filename = file_name + '_480p_%03d.ts'

    source_linux = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_linux = "/mnt/" + target.replace("\\", "/").replace("C:", "c")
    segment_filename_linux = "/mnt/" + segment_filename.replace("\\", "/").replace("C:", "c")

    cmd = 'ffmpeg -i "{}" \-vf scale=-2:480 -c:v h264 -b:v 1000k -c:a aac -b:a 128k -hls_time 6 -hls_playlist_type vod -hls_segment_filename "{}" "{}"'.format(source_linux,segment_filename_linux, target_linux)
    subprocess.run(cmd, capture_output=True, shell=True)

def delete_video_files(video_id):
    delete_preview(video_id)
    delete_thumbnail(video_id)
    delete_HLS_segments(video_id)

def delete_preview(video_id):
    target_directory = os.path.join('media', 'previews', str(video_id))
    shutil.rmtree(target_directory)

def delete_thumbnail(video_id):
    target_directory = os.path.join('media', 'thumbnails', str(video_id))
    shutil.rmtree(target_directory)

def delete_HLS_segments(video_id):
    target_directory = os.path.join('media', 'videos', str(video_id))
    shutil.rmtree(target_directory)