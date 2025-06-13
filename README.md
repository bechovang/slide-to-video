# slide-to-video


# Slide-to-Video Project

Dự án này chuyển đổi file **PDF slide** thành video full HD với âm thanh (audio) và phụ đề. Các slide từ file PDF sẽ được sử dụng làm hình ảnh trong video, đồng thời phụ đề sẽ được hiển thị đúng thời gian dựa trên thông tin từ file **SRT**.

## Tính năng

- **Chuyển đổi PDF thành hình ảnh**: Mỗi trang trong file PDF sẽ được chuyển thành một hình ảnh.
- **Kết hợp âm thanh và hình ảnh**: Âm thanh từ file **`.wav`** sẽ được kết hợp với các hình ảnh từ slide để tạo thành video.
- **Thêm phụ đề (SRT)**: Phụ đề được lấy từ file **`.srt`** và hiển thị đúng thời gian, không bị đè lên slide.
- **Tạo 2 video**:
  - **Video không có phụ đề**.
  - **Video có phụ đề**.

## Yêu cầu

1. **Python 3.x**.
2. **Các thư viện Python**: Cài đặt các thư viện cần thiết bằng lệnh:
    ```bash
    pip install -r requirements.txt
    ```

3. **File đầu vào**:
   - **PDF**: File slide cần chuyển thành video (ví dụ: `slide.pdf`).
   - **Audio**: File âm thanh đi kèm cho video (ví dụ: `audio.wav`).
   - **SRT**: File phụ đề tương ứng với âm thanh (ví dụ: `script.srt`).

## Cài đặt

1. **Cài đặt thư viện Python**:
    - Tạo môi trường ảo (virtual environment) và kích hoạt nó:
      ```bash
      python -m venv venv
      # Windows
      .\venv\Scripts\activate
      # macOS/Linux
      source venv/bin/activate
      ```

    - Cài đặt các thư viện cần thiết:
      ```bash
      pip install -r requirements.txt
      ```

2. **Đặt file đầu vào**:
    - Đảm bảo rằng bạn có các file sau trong thư mục dự án:
        - `slide.pdf`: File slide (PDF).
        - `audio.wav`: File âm thanh.
        - `script.srt`: File phụ đề SRT.

3. **Chạy mã Python**:
    - Chạy script để tạo video:
    ```bash
    python main.py
    ```

4. **Kết quả**:
    - Sau khi chạy xong, bạn sẽ nhận được hai video:
        - **`no_sub_output_video.mp4`**: Video không có phụ đề.
        - **`output_video.mp4`**: Video có phụ đề.

## Lưu ý

- **Kích thước video**: Video được tạo ở độ phân giải **Full HD (1920x1080)**.
- **Font phụ đề**: Bạn có thể thay đổi font trong mã nếu muốn thay đổi cách hiển thị phụ đề.
- **Xử lý lỗi**: Đảm bảo rằng file PDF, âm thanh và phụ đề đã được chuẩn bị đúng định dạng.

## Giới thiệu

Dự án này sử dụng các thư viện Python sau:
- **`moviepy`**: Dùng để chỉnh sửa video, kết hợp âm thanh và hình ảnh, thêm phụ đề.
- **`pdf2image`**: Chuyển đổi PDF thành hình ảnh.
- **`pysrt`**: Đọc và xử lý phụ đề từ file `.srt`.

## Cách sử dụng

1. **Chuẩn bị các file**:
    - Đặt file PDF slide, file âm thanh và file phụ đề vào thư mục dự án.
   
2. **Chạy script**:
    - Chạy `main.py` để bắt đầu quá trình tạo video từ các file này.

3. **Kết quả**:
    - Bạn sẽ nhận được hai video: một video có phụ đề và một video không có phụ đề.

## Tạo video với phụ đề
```bash
python main.py
````

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc đóng góp nào, đừng ngần ngại liên hệ.

---
