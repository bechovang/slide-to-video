import os
import time
from pdf2image import convert_from_path
from moviepy.editor import *
import pysrt

# === Chuyển PDF thành hình ảnh ===
def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    image_files = []
    for i, image in enumerate(images):
        image_path = f"slide_{i + 1}.png"
        image.save(image_path, "PNG")
        image_files.append(image_path)
    return image_files

# === Đọc thời gian từ file time_transactions.txt ===
def read_time_transactions(time_file):
    time_trans = []
    with open(time_file, 'r') as f:
        for line in f:
            start_time, end_time = line.strip().split(" - ")
            time_trans.append((start_time, end_time))
    return time_trans

# === Thêm phụ đề vào video ===
def add_subtitles_to_video(video, subtitles):
    subtitle_clips = []
    for subtitle in subtitles:
        start_time = subtitle.start.total_seconds()
        end_time = subtitle.end.total_seconds()
        text = subtitle.text
        
        subtitle_clip = TextClip(text, fontsize=24, color='white', bg_color='black', font="Arial-Bold", size=video.size)
        subtitle_clip = subtitle_clip.set_position('bottom').set_duration(end_time - start_time).set_start(start_time)
        subtitle_clips.append(subtitle_clip)

    return CompositeVideoClip([video] + subtitle_clips)

# === Tạo video từ slide và âm thanh ===
def create_video_from_slides_and_audio(slide_images, audio_path, time_transactions, output_video_path):
    # Load audio file
    audio = AudioFileClip(audio_path)

    # Tạo video clips từ slides và áp dụng thời gian từ time_transactions.txt
    slide_clips = []
    for i, slide_img in enumerate(slide_images):
        start_time_str, end_time_str = time_transactions[i]
        start_time = convert_time_to_seconds(start_time_str)
        end_time = convert_time_to_seconds(end_time_str)

        slide_clip = ImageClip(slide_img).set_duration(end_time - start_time).set_start(start_time)
        slide_clips.append(slide_clip)
    
    # Tạo video từ các slide clips
    video = concatenate_videoclips(slide_clips, method="compose")
    video = video.set_audio(audio)

    return video

# === Chuyển đổi thời gian từ dạng HH:MM:SS thành giây ===
def convert_time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(":"))
    return hours * 3600 + minutes * 60 + seconds

# === Đọc phụ đề từ file SRT ===
def read_subtitles_from_srt(srt_path):
    subtitles = pysrt.open(srt_path)
    return subtitles

# === Kết hợp tất cả lại ===
def generate_video(pdf_path, audio_path, srt_path, time_file, output_video_path):
    print("Chuyển đổi PDF thành hình ảnh...")
    slide_images = convert_pdf_to_images(pdf_path)

    print("Đọc thời gian từ time_transactions.txt...")
    time_transactions = read_time_transactions(time_file)

    print("Đọc phụ đề từ SRT...")
    subtitles = read_subtitles_from_srt(srt_path)

    print("Tạo video từ slide và âm thanh...")
    video = create_video_from_slides_and_audio(slide_images, audio_path, time_transactions, output_video_path)

    # Tạo video không có phụ đề
    video.write_videofile(f"no_sub_{output_video_path}", codec="libx264", fps=24)

    print("Thêm phụ đề vào video...")
    video_with_subtitles = add_subtitles_to_video(video, subtitles)

    print(f"Lưu video với phụ đề ở {output_video_path}...")
    video_with_subtitles.write_videofile(output_video_path, codec="libx264", fps=24)

# === Chạy toàn bộ quá trình ===
if __name__ == "__main__":
    pdf_path = "slide.pdf"  # Đường dẫn đến file slide PDF
    audio_path = "audio.wav"  # Đường dẫn đến file âm thanh
    srt_path = "script.srt"  # Đường dẫn đến file phụ đề SRT
    time_file = "time_transactions.txt"  # Đường dẫn đến file time transactions
    output_video_path = "output_video.mp4"  # Đường dẫn tới video đầu ra có phụ đề

    generate_video(pdf_path, audio_path, srt_path, time_file, output_video_path)
