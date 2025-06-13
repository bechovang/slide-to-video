import os
import time
import fitz
from moviepy.editor import *
import pysrt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import textwrap

def format_duration(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{int(mins)} phút, {secs:.2f} giây"

def convert_pdf_to_images(pdf_path):
    print("  ...Sử dụng PyMuPDF để chuyển đổi.")
    doc = fitz.open(pdf_path)
    image_files = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        image_path = f"slide_{i + 1}.png"
        pix.save(image_path)
        image_files.append(image_path)
    doc.close()
    return image_files

def read_time_transactions(time_file):
    time_trans = []
    with open(time_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                start_time, end_time = line.strip().split(" - ")
                time_trans.append((start_time, end_time))
    return time_trans

def subriptime_to_seconds(srt_time):
    return srt_time.hours * 3600 + srt_time.minutes * 60 + srt_time.seconds + srt_time.milliseconds / 1000.0

def add_subtitles_to_video(video, subtitles):
    subtitle_clips = []
    
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        print("Font Arial không tồn tại, sử dụng font mặc định.")
        font = ImageFont.load_default()

    for sub in subtitles:
        start_time = subriptime_to_seconds(sub.start)
        end_time = subriptime_to_seconds(sub.end)
        duration = end_time - start_time
        text = sub.text

        wrapped_text = "\n".join(textwrap.wrap(text, width=50))
        
        temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
        try:
            # Phiên bản Pillow mới hơn
            text_bbox = temp_draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        except AttributeError:
            # Phiên bản Pillow cũ hơn
            text_width, text_height = temp_draw.textsize(wrapped_text, font=font)

        img_width = int(video.w * 0.9)
        img_height = text_height + 20 
        
        img = Image.new('RGB', (img_width, img_height), color='black')
        d = ImageDraw.Draw(img)
        
        d.text(((img_width - text_width) / 2, 10), wrapped_text, font=font, fill='white', align='center')
        
        subtitle_img = np.array(img)
        
        subtitle_clip = ImageClip(subtitle_img)\
            .set_duration(duration)\
            .set_start(start_time)\
            .set_position(('center', 'bottom'))
            
        subtitle_clips.append(subtitle_clip)

    return CompositeVideoClip([video] + subtitle_clips)

# SỬA ĐỔI: Hàm này được cập nhật để đảm bảo kích thước video là số chẵn
def create_video_from_slides_and_audio(slide_images, audio_path, time_transactions):
    audio = AudioFileClip(audio_path)
    
    # Lấy kích thước từ slide đầu tiên
    first_slide_size = ImageClip(slide_images[0]).size
    width, height = first_slide_size
    
    # Đảm bảo chiều rộng và chiều cao là số chẵn
    final_width = width - (width % 2)
    final_height = height - (height % 2)
    final_size = (final_width, final_height)
    print(f"-> Kích thước slide gốc: {width}x{height}. Điều chỉnh thành: {final_width}x{final_height} để tương thích.")

    slide_clips = []
    total_duration = 0
    for i, slide_img in enumerate(slide_images):
        start_time_str, end_time_str = time_transactions[i]
        start_time = convert_time_to_seconds(start_time_str)
        end_time = convert_time_to_seconds(end_time_str)
        duration = end_time - start_time
        
        if end_time > total_duration:
            total_duration = end_time

        # Tạo slide clip và resize về kích thước chẵn đã tính
        slide_clip = ImageClip(slide_img)\
            .set_duration(duration)\
            .set_start(start_time)\
            .resize(final_size)
            
        slide_clips.append(slide_clip)
    
    # Tạo video cuối cùng với kích thước đã được làm chẵn
    video = CompositeVideoClip(slide_clips, size=final_size)
    video = video.set_duration(total_duration)
    video = video.set_audio(audio)
    return video

def convert_time_to_seconds(time_str):
    clean_str = time_str.strip().replace(',', '.')
    parts = clean_str.split(':')
    
    if len(parts) == 3:
        h, m, s = int(parts[0]), int(parts[1]), float(parts[2])
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:
        m, s = int(parts[0]), float(parts[1])
        return m * 60 + s
    elif len(parts) == 1:
        return float(parts[0])
    return 0.0

def read_subtitles_from_srt(srt_path):
    subtitles = pysrt.open(srt_path, encoding='utf-8')
    return subtitles

def generate_video(pdf_path, audio_path, srt_path, time_file, output_video_path):
    last_step_time = time.time()

    print("1. Chuyển đổi PDF thành hình ảnh...")
    slide_images = convert_pdf_to_images(pdf_path)
    current_time = time.time()
    print(f"-> Hoàn thành sau: {format_duration(current_time - last_step_time)}\n")
    last_step_time = current_time

    print("2. Đọc thời gian và phụ đề...")
    time_transactions = read_time_transactions(time_file)
    subtitles = read_subtitles_from_srt(srt_path)
    current_time = time.time()
    print(f"-> Hoàn thành sau: {format_duration(current_time - last_step_time)}\n")
    last_step_time = current_time

    print("3. Tạo video từ slide và âm thanh (chưa có phụ đề)...")
    video = create_video_from_slides_and_audio(slide_images, audio_path, time_transactions)
    current_time = time.time()
    print(f"-> Hoàn thành sau: {format_duration(current_time - last_step_time)}\n")
    last_step_time = current_time

    no_sub_path = f"no_sub_{output_video_path}"
    print(f"4. Đang lưu video không có phụ đề vào '{no_sub_path}'...")
    ffmpeg_params = ['-pix_fmt', 'yuv420p']
    video.write_videofile(no_sub_path, codec="libx264", fps=24, threads=4, logger='bar', ffmpeg_params=ffmpeg_params)
    current_time = time.time()
    print(f"-> Hoàn thành sau: {format_duration(current_time - last_step_time)}\n")
    last_step_time = current_time

    print("5. Thêm phụ đề vào video...")
    # Nạp lại video từ file vừa lưu để đảm bảo sự ổn định
    video_reloaded = VideoFileClip(no_sub_path)
    video_with_subtitles = add_subtitles_to_video(video_reloaded, subtitles)
    current_time = time.time()
    print(f"-> Hoàn thành sau: {format_duration(current_time - last_step_time)}\n")
    last_step_time = current_time

    print(f"6. Đang lưu video có phụ đề vào '{output_video_path}'...")
    video_with_subtitles.write_videofile(output_video_path, codec="libx264", fps=24, threads=4, logger='bar', ffmpeg_params=ffmpeg_params)
    current_time = time.time()
    print(f"-> Hoàn thành sau: {format_duration(current_time - last_step_time)}\n")

if __name__ == "__main__":
    pdf_path = "slide.pdf"
    audio_path = "audio.wav"
    srt_path = "script.srt"
    time_file = "time_transactions.txt"
    output_video_path = "output_video.mp4"

    total_start_time = time.time()
    print("=============================================")
    print("=== BẮT ĐẦU QUÁ TRÌNH TẠO VIDEO TỰ ĐỘNG ===")
    print("=============================================\n")

    generate_video(pdf_path, audio_path, srt_path, time_file, output_video_path)

    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    print("\n==============================================")
    print("=== HOÀN TẤT TOÀN BỘ QUÁ TRÌNH ===")
    print(f"Tổng thời gian thực hiện: {format_duration(total_duration)}")
    print("==============================================")