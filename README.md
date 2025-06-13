

# Slide-to-Video Project

Dự án này chuyển đổi file **PDF slide** thành video full HD với âm thanh (audio) và phụ đề. Các slide từ file PDF sẽ được sử dụng làm hình ảnh trong video, đồng thời phụ đề sẽ được hiển thị đúng thời gian dựa trên thông tin từ file **SRT**. Bạn cũng có thể xác định thời gian chuyển slide thông qua **file `time_transactions.txt`**.

## Tính năng

* **Chuyển đổi PDF thành hình ảnh**: Mỗi trang trong file PDF sẽ được chuyển thành một hình ảnh.
* **Kết hợp âm thanh và hình ảnh**: Âm thanh từ file **`.wav`** sẽ được kết hợp với các hình ảnh từ slide để tạo thành video.
* **Thêm phụ đề (SRT)**: Phụ đề được lấy từ file **`.srt`** và hiển thị đúng thời gian, không bị đè lên slide.
* **Thời gian chuyển slide**: Thời gian hiển thị của mỗi slide được lấy từ file **`time_transactions.txt`** để điều chỉnh thời gian hiển thị của các slide.
* **Tạo 2 video**:

  * **Video không có phụ đề**.
  * **Video có phụ đề**.

## Yêu cầu

1. **Python 3.x**

2. **Các thư viện Python cần thiết**: Cài đặt các thư viện cần thiết bằng lệnh:

   ```bash
   pip install -r requirements.txt
   ```

3. **File đầu vào**:

   * **PDF**: File slide cần chuyển thành video (ví dụ: `slide.pdf`).
   * **Audio**: File âm thanh đi kèm cho video (ví dụ: `audio.wav`).
   * **SRT**: File phụ đề tương ứng với âm thanh (ví dụ: `script.srt`).
   * **Time Transactions**: File **`time_transactions.txt`** để xác định thời gian chuyển slide.

## Định dạng của file `time_transactions.txt`

File **`time_transactions.txt`** chứa thông tin về **thời gian chuyển slide**. Mỗi dòng trong file sẽ chứa khoảng thời gian mà một slide sẽ hiển thị trong video. Định dạng của file như sau:

```
00:00:00 - 00:10:00
00:10:00 - 00:20:00
00:20:00 - 00:30:00
...
```

### Cấu trúc:

* **Mỗi dòng** chứa hai giá trị thời gian: **start time** và **end time**.
* **Start time** là thời gian bắt đầu hiển thị của một slide (theo định dạng `HH:MM:SS`).
* **End time** là thời gian kết thúc hiển thị của một slide (theo định dạng `HH:MM:SS`).
* Mỗi dòng sẽ có một khoảng thời gian cho một slide hiển thị. Thời gian của mỗi slide được tính bằng giây và căn cứ vào thời gian bắt đầu và kết thúc.

### Ví dụ:

```
00:00:00 - 00:10:00   # Slide 1 hiển thị từ 0:00 đến 0:10
00:10:00 - 00:20:00   # Slide 2 hiển thị từ 0:10 đến 0:20
00:20:00 - 00:30:00   # Slide 3 hiển thị từ 0:20 đến 0:30
00:30:00 - 00:40:00   # Slide 4 hiển thị từ 0:30 đến 0:40
```

### Lưu ý:

* **Sắp xếp thời gian**: Đảm bảo rằng các khoảng thời gian không bị trùng lặp hoặc không hợp lệ (tức là `end time` của slide này phải lớn hơn `start time` của slide trước đó).
* **Đảm bảo đủ thời gian cho mỗi slide**: Tổng thời gian của các slide phải tương đương với độ dài của âm thanh trong video. Nếu file âm thanh dài 3 phút, tổng thời gian của các slide phải là 3 phút.

## Cài đặt và sử dụng

### 1. Tạo Virtual Environment (venv)

Trước khi bắt đầu, hãy tạo một **virtual environment** để quản lý các thư viện Python.

#### Trên Windows:

```bash
python -m venv venv
```

#### Trên macOS/Linux:

```bash
python3 -m venv venv
```

### 2. Kích hoạt Virtual Environment

#### Trên Windows:

```bash
.\venv\Scripts\activate
```

#### Trên macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Cài đặt các thư viện cần thiết

Sau khi kích hoạt **virtual environment**, cài đặt các thư viện cần thiết bằng lệnh sau:

```bash
pip install -r requirements.txt
```

### 4. Đặt file đầu vào

* Đảm bảo rằng bạn có các file sau trong thư mục dự án:

  * `slide.pdf`: File slide (PDF).
  * `audio.wav`: File âm thanh.
  * `script.srt`: File phụ đề SRT.
  * `time_transactions.txt`: File xác định thời gian chuyển slide.

### 5. Chạy mã Python

Khi tất cả đã được cài đặt và cấu hình, chỉ cần chạy file Python để thực hiện nhận diện giọng nói từ file âm thanh.

```bash
python main.py
```

### 6. Kết quả

Sau khi quá trình nhận diện kết thúc, bạn sẽ nhận được hai video:

1. **`no_sub_output_video.mp4`**: Video không có phụ đề.
2. **`output_video.mp4`**: Video có phụ đề.

---

## Giới thiệu

Dự án này sử dụng các thư viện Python sau:

* **`moviepy`**: Dùng để chỉnh sửa video, kết hợp âm thanh và hình ảnh, thêm phụ đề.
* **`pdf2image`**: Chuyển đổi PDF thành hình ảnh.
* **`pysrt`**: Đọc và xử lý phụ đề từ file `.srt`.

## Cách sử dụng

1. **Chuẩn bị các file**:

   * Đặt file PDF slide, file âm thanh, file phụ đề, và file thời gian chuyển slide (`time_transactions.txt`) vào thư mục dự án.

2. **Chạy script**:

   * Chạy `main.py` để bắt đầu quá trình tạo video từ các file này.

3. **Kết quả**:

   * Bạn sẽ nhận được hai video: một video có phụ đề và một video không có phụ đề.

## Liên hệ

Nếu bạn có bất kỳ câu hỏi hoặc đóng góp nào, đừng ngần ngại liên hệ.

---

### Giải thích các phần trong README:

* **Tính năng**: Mô tả các tính năng chính của dự án.
* **Yêu cầu**: Các phần mềm và thư viện cần thiết để chạy dự án.
* **Cài đặt và sử dụng**: Hướng dẫn từng bước cài đặt và chạy dự án.
* **Giới thiệu**: Giới thiệu về các thư viện được sử dụng trong dự án.
* **Định dạng `time_transactions.txt`**: Mô tả cấu trúc của file `time_transactions.txt` để người dùng hiểu cách cung cấp thời gian cho các slide.
