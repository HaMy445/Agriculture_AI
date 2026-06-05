<h1 align="center">
🌾 Hệ Thống Phát Hiện Bệnh Lúa Thông Minh (AI_Agri)
</h1>

<div align="center">
  <img src="https://img.icons8.com/color/96/000000/leaf.png" alt="Leaf Icon" width="120">
</div>

<br>

<div align="center">

[![Flask](https://img.shields.io/badge/-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](#)
[![YOLOv8](https://img.shields.io/badge/-YOLOv8-00979D?style=for-the-badge&logo=python&logoColor=white)](#)
[![Groq](https://img.shields.io/badge/-Groq%20LLM-F7931E?style=for-the-badge)](#)
[![Python](https://img.shields.io/badge/-Python%203.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![OpenCV](https://img.shields.io/badge/-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](#)

</div>

<hr>

<h2 align="center">✨ Giới Thiệu Dự Án</h2>

<p align="justify">
  <strong>AI_Agri</strong> là hệ thống <strong>phát hiện bệnh lúa tự động</strong> sử dụng công nghệ <strong>Deep Learning (YOLOv8)</strong> kết hợp với <strong>AI tư vấn tiếng Việt (Groq LLM)</strong>. Hệ thống cung cấp:
  <br><br>
  ✅ <strong>Phát hiện bệnh lúa chính xác</strong> - YOLOv8 nhận diện 5 loại bệnh với bounding boxes<br>
  ✅ <strong>Tư vấn điều trị tiếng Việt</strong> - Groq AI cung cấp lời khuyên chi tiết<br>
  ✅ <strong>Ghi lại lịch sử</strong> - JSON local records với metadata đầy đủ<br>
  ✅ <strong>Cảnh báo email tự động</strong> - Thông báo khi phát hiện bệnh<br>
  ✅ <strong>Giao diện web thân thiện</strong> - Flask API + HTML5 responsive design<br>
  ✅ <strong>Hỗ trợ mobile</strong> - Có thể chụp ảnh trực tiếp từ điện thoại<br>
</p>

<hr>

<h2 align="center">🍚 5 Loại Bệnh Lúa Được Phát Hiện</h2>

<div align="center">
<table>
  <tr>
    <th>#</th>
    <th>Tên Bệnh</th>
    <th>Tên Khoa Học</th>
    <th>Triệu Chứng & Tác Động</th>
  </tr>
  <tr>
    <td>1</td>
    <td><strong>🟢 Bệnh Bạc lá</strong></td>
    <td><em>Xanthomonas oryzae</em></td>
    <td>Lá vàng → bạc, mềm, ẩm. Gây mất năng suất 20-50%</td>
  </tr>
  <tr>
    <td>2</td>
    <td><strong>🟤 Bệnh Đốm nâu</strong></td>
    <td><em>Helminthosporium oryzae</em></td>
    <td>Đốm nâu hình bầu dục trên lá. Làm héo úa lá sớm</td>
  </tr>
  <tr>
    <td>3</td>
    <td><strong>🔴 Bệnh Đạo ôn</strong></td>
    <td><em>Pyricularia oryzae</em></td>
    <td>Vệt khô từ lá non → lá già. Ảnh hưởng thóc chắc</td>
  </tr>
  <tr>
    <td>4</td>
    <td><strong>🟡 Bệnh Khô vằn</strong></td>
    <td><em>Fusarium/Rhizoctonia</em></td>
    <td>Vằn khô vàng/nâu trên lá bẹ. Gây hạt không đầy</td>
  </tr>
  <tr>
    <td>5</td>
    <td><strong>🟢 Lá Khỏe Mạnh</strong></td>
    <td>-</td>
    <td>Không có dấu hiệu bệnh. Sinh trưởng bình thường</td>
  </tr>
</table>
</div>

<hr>

<h2 align="center">📁 Cấu Trúc Dự Án</h2>

<pre align="center">
📂 AI_Agri/
├── 📄 <strong>app_flask.py</strong>              # Flask API Backend (Port 5000) ⭐
├── 🌐 <strong>index.html</strong>               # Main Web Interface
├── 📱 <strong>phone.html</strong>               # Mobile Responsive UI
├── 📦 <strong>requirements.txt</strong>        # Python Dependencies
├── 🤖 models/
│   └── <strong>best.pt</strong>                # YOLOv8 Pretrained Model
├── 📊 dataset/
│   ├── train/  (Training images & labels)
│   ├── valid/  (Validation images)
│   └── test/   (Test images)
├── 💾 history/
│   ├── <strong>data.json</strong>              # Local Records Database
│   ├── images/                     # Original & Annotated Images
│   └── phone_uploads/              # Mobile Uploads
├── 📚 Documentation/
│   ├── README.md                   # This file
│   ├── SYSTEM_ARCHITECTURE.md      # Detailed Architecture
│   └── RUN_COMMANDS.md             # Setup Commands
└── 📝 requirements.txt             # Dependencies
</pre>

<hr>

<h2 align="center">📦 Yêu Cầu Hệ Thống</h2>

### Phần Mềm & Công Nghệ

- **OS**: Windows 10/11, macOS, hoặc Linux
- **Python**: 3.8+ (khuyến nghị 3.10+)
- **RAM**: 4GB+ (8GB được khuyến nghị)
- **Storage**: 3GB trống
- **GPU**: Optional (tăng tốc độ phát hiện)

<hr>

<h2 align="center">🚀 Hướng Dẫn Cài Đặt & Chạy</h2>

### Bước 1: Tạo Virtual Environment

```powershell
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Bước 2: Cài Đặt Python Packages

```powershell
pip install -r requirements.txt
```

**Hoặc cài thủ công:**

```powershell
pip install Flask>=2.0.0
pip install flask-cors>=3.0.10
pip install ultralytics>=8.0.0
pip install groq>=0.4.0
pip install pillow>=10.0.0
pip install opencv-python>=4.8.0
pip install numpy>=1.24.0
pip install requests>=2.31.0
```

### Bước 3: Cấu Hình Groq API Key

1. Lấy API Key từ: https://console.groq.com/
2. Mở `app_flask.py`, dòng ~30:

```python
GROQ_API_KEY = "gsk_your_api_key_here"
client_groq = Groq(api_key=GROQ_API_KEY)
```

### Bước 4: Chạy Flask Server

```powershell
python app_flask.py

# Server running at: http://localhost:5000
```

### Bước 5: Mở Ứng Dụng

Mở trình duyệt: **http://localhost:5000**

<hr>

<h2 align="center">📋 API Endpoints</h2>

<div align="center">
<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Input</th>
    <th>Output</th>
    <th>Mô Tả</th>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/</code></td>
    <td>-</td>
    <td>HTML</td>
    <td>Serve trang chính (index.html)</td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/health</code></td>
    <td>-</td>
    <td>JSON: {status}</td>
    <td>Kiểm tra server sống</td>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/detect</code></td>
    <td>image (file)</td>
    <td>diseases[], advice, bbox, image_base64</td>
    <td><strong>⭐ Phát hiện bệnh + vẽ bbox</strong></td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/api/history/get</code></td>
    <td>-</td>
    <td>records[], total</td>
    <td>Lấy tất cả lịch sử</td>
  </tr>
  <tr>
    <td>POST</td>
    <td><code>/api/history/save-local</code></td>
    <td>timestamp, results</td>
    <td>{success}</td>
    <td>Lưu record vào file</td>
  </tr>
  <tr>
    <td>GET</td>
    <td><code>/history/images/*</code></td>
    <td>filename</td>
    <td>image file</td>
    <td>Phục vụ hình ảnh</td>
  </tr>
</table>
</div>

<hr>

<h2 align="center">🔄 Luồng Xử Lý Dữ Liệu (Data Flow)</h2>

<pre align="center">
┌─────────────────────────────────────────┐
│  1. User Upload Image (Frontend)        │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  2. POST /api/detect                    │
│     - Save original image               │
│     - Calculate SHA256 hash             │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  3. YOLOv8 Inference                    │
│     - Load models/best.pt               │
│     - Predict diseases + confidence     │
│     - Extract bounding boxes            │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  4. Groq AI Advisory (Vietnamese)       │
│     - For each disease:                 │
│     - Send Vietnamese prompt            │
│     - Get treatment recommendations     │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  5. Extract Medications                 │
│     - Parse advice text                 │
│     - Find drug names (regex + keywords)│
│     - Return max 5 medications          │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  6. Draw Bounding Boxes (PIL + Font)    │
│     - Support Vietnamese text           │
│     - Color code by disease             │
│     - Save annotated image              │
│     - Convert to Base64                 │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  7. Save to Local History (JSON)        │
│     - history/data.json                 │
│     - Store all metadata                │
│     - Save timestamp & image hash       │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  8. Send Email Notification             │
│     - Only if NOT "Lá khỏe mạnh"       │
│     - Gmail SMTP (port 587)             │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  9. Return JSON Response to Frontend    │
│     - diseases[], advice, medications   │
│     - image_base64 (for display)        │
│     - timestamp, boxes info             │
└─────────────────────────────────────────┘
</pre>

<hr>

<h2 align="center">🧠 Các Thành Phần Chính</h2>

### I. Backend (`app_flask.py`)

**Port**: 5000  
**Framework**: Flask + CORS

**Các Hàm Chính:**

```python
# 1. Phát hiện bệnh
POST /api/detect
  ├─ Nhận: image file
  ├─ YOLOv8 predict(conf=0.5, imgsz=640)
  ├─ Output: [diseases[], confidence[], bbox[]]
  └─ Return: JSON + base64 image

# 2. Tư vấn AI
get_treatment_advice(disease_name_vi)
  ├─ Model: llama-3.3-70b-versatile
  ├─ Prompt: "Bạn là chuyên gia nông nghiệp VN..."
  └─ Output: Vietnamese treatment text

# 3. Extract thuốc
extract_medications(advice_text)
  ├─ Parse lines with "-" hoặc "*"
  ├─ Regex: Azoxystrobin, Tebuconazole, etc.
  └─ Output: medications[] (max 5)

# 4. Vẽ Bounding Boxes (PIL)
draw_bounding_boxes(image, boxes_info)
  ├─ Load font: arial.ttf (Windows)
  ├─ For each box:
  │  ├─ Draw rectangle (color by disease)
  │  ├─ Draw label + confidence
  │  └─ Draw background box
  └─ Output: annotated_image_base64

# 5. Lưu Local
save_to_history(...)
  ├─ Record: {id, time, diseases, medications, 
  │            image_path, image_hash, advice}
  └─ File: history/data.json

# 6. Gửi Email
send_email_notification(diseases, advice)
  ├─ SMTP: smtp.gmail.com:587
  ├─ From: wuveil215@gmail.com
  └─ Only if NOT "Lá khỏe mạnh"
```

### II. Frontend (`index.html`)

**Features:**
- ✅ Drag-Drop Image Upload
- ✅ Real-time Results Display
- ✅ Bounding Box Visualization
- ✅ History Management
- ✅ Responsive Design
- ✅ Mobile Support (phone.html)

**Key Components:**
1. Navbar: Logo + Status Badge
2. Upload Section: Drag-drop + Preview
3. Results Card: Annotated image + Advice
4. Diseases List: With confidence badges
5. Medications: Treatment recommendations
6. History Table: All detection records

### III. YOLOv8 Model

**Model**: `models/best.pt`  
**Input**: Image (640x640 px)  
**Output**: Bounding boxes + class labels + confidence  
**Classes**: 5 disease types + healthy leaf

<hr>

<h2 align="center">📸 Cách Sử Dụng Hệ Thống</h2>

### Bước 1: Upload Ảnh

- Nhấn "Upload Image" hoặc kéo thả ảnh
- Chọn file từ máy tính (JPEG, PNG, JPG)
- Hoặc chụp ảnh trực tiếp từ điện thoại (qua phone.html)

### Bước 2: Xem Kết Quả

- **Ảnh Annotated**: Ảnh được vẽ bounding box cho từng bệnh
- **Loại Bệnh**: Tên bệnh được phát hiện
- **Confidence**: Độ tin cậy (%)
- **Tư Vấn AI**: Lời khuyên chi tiết từ Groq

### Bước 3: Xem Lời Khuyên

- **Thuốc Khuyến Nghị**: Danh sách thuốc điều trị
- **Hướng Dẫn Chi Tiết**: Từ Groq AI tiếng Việt
- **Dự Phòng**: Cách phòng chống bệnh

### Bước 4: Lưu Lịch Sử

- Tất cả kết quả tự động lưu vào `history/data.json`
- Xem lịch sử trên tab "History"
- Tải xuống ảnh annotated nếu cần

<hr>

<h2 align="center">🔐 Bảo Mật & Cấu Hình</h2>

### Groq API Key

```python
# Trong app_flask.py
GROQ_API_KEY = "gsk_your_api_key_here"  # Lấy từ https://console.groq.com/
```

### Email Notifications (Tùy Chọn)

```python
# app_flask.py
sender_email = "wuveil215@gmail.com"
receiver_email = "hamy5dvdsz@gmail.com"
app_password = "kkeu aaum yikq zqlo"
```

⚠️ **Lưu ý**: Bật 2-Factor Authentication và tạo App Password trên Gmail

### Security Best Practices

```bash
# 1. Create .env file
echo "GROQ_API_KEY=your_key_here" > .env
echo "GMAIL_PASSWORD=your_password_here" >> .env

# 2. Load from environment
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 3. Don't commit .env to git
echo ".env" >> .gitignore
```

<hr>

<h2 align="center">🐛 Troubleshooting</h2>

### Lỗi: ModuleNotFoundError

```bash
# Giải pháp:
pip install -r requirements.txt
```

### Lỗi: Port 5000 đã được sử dụng

```bash
# Giải pháp 1: Dùng port khác
python app_flask.py --port 5001

# Giải pháp 2: Tìm và kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Lỗi: Model file not found

```bash
# Kiểm tra:
# - File models/best.pt tồn tại
# - Đường dẫn đúng trong app_flask.py
```

### Lỗi: Out of memory

```bash
# Giải pháp:
# 1. Tăng RAM
# 2. Giảm input image size (imgsz=416)
# 3. Sử dụng GPU (CUDA)
```

### Lỗi: Groq API Error

```bash
# Kiểm tra:
# 1. API key đúng
# 2. Internet connection sống
# 3. Groq quota còn
```

<hr>

<h2 align="center">📚 Tài Liệu Tham Khảo</h2>

- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - Kiến trúc chi tiết
- [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - Mermaid diagrams
- [RUN_COMMANDS.md](RUN_COMMANDS.md) - Lệnh khởi động
- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Groq API Documentation](https://console.groq.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

<hr>

<h2 align="center">🤝 Đóng Góp & Hỗ Trợ</h2>

- **Issues**: Báo cáo lỗi trên GitHub Issues
- **Discussions**: Thảo luận về features mới
- **Pull Requests**: Gửi code improvements

<hr>

<h2 align="center">📝 License & Terms</h2>

**License**: CC BY 4.0 - Agricultural Research  
**Author**: AI_Agri Team  
**Year**: 2024  
**Status**: Active Development

---

<div align="center">
  <h3>✨ Cảm Ơn Vì Đã Sử Dụng AI_Agri ✨</h3>
  <p><strong>Chúc các bạn nông dân có năng suất lúa cao và bệnh tật ít hơn!</strong></p>
  <p><strong>🌾 Happy Farming! 🌾</strong></p>
</div>

---

**Phiên bản**: 2.0 (Focused on Disease Detection)  
**Cập nhật lần cuối**: 2024  
**Tác giả**: AI_Agri Development Team  
**Ngôn ngữ**: Tiếng Việt

© 2024 AI_Agri. All rights reserved.
