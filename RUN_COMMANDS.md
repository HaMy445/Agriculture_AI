# 🚀 AI_Agri - Câu Lệnh Chạy Ứng Dụng

## ⚡ 4 Bước Chạy (4 Terminal)

### **Terminal 1️⃣: Ganache (Blockchain Local)**
```powershell
ganache --host 127.0.0.1 --port 8545 --deterministic
```
✅ **GIỮ CHẠY** - Đừng đóng terminal này
- Port: 8545
- Deterministic: Khóa seed cố định (account giống nhau mỗi lần)

---

### **Terminal 2️⃣: Deploy Smart Contract**
```powershell
cd c:\Users\Admin\Desktop\AI_Agri\blockchain
truffle migrate --network development
```
📝 **Chạy lần đầu hoặc khi cần reset**
- Compile & deploy contract lên Ganache
- Copy địa chỉ contract nếu có thay đổi

---

### **Terminal 3️⃣: Flask API Server**
```powershell
cd c:\Users\Admin\Desktop\AI_Agri
python app_flask.py
```
🌐 **API chạy tại port 5000**
- Endpoint: `http://localhost:5000`
- API Routes: `/api/detect`, `/api/blockchain/*`, etc.

---

### **Terminal 4️⃣: HTTP Server (Tùy Chọn)**
```powershell
python -m http.server 8000
```
📁 **Serve file tĩnh tại port 8000** (tùy chọn)
- Access: `http://localhost:8000/index.html`
- **Khuyến nghị**: Chỉ dùng Terminal 1-3 là đủ

---

## 🎯 Mở Ứng Dụng

### **Cách 1: Máy Tính (Phát Hiện Bệnh)**
```
http://localhost:5000
```

### **Cách 2: Điện Thoại (Chụp & Gửi Ảnh)** 🔥 **MỚI**
1. Nhập trên điện thoại:
```
http://192.168.111.55:5000/phone.html
(thay 192.168.111.55 bằng IP của PC)
```

2. **Trên điện thoại**:
   - 📷 Chụp ảnh lá lúa
   - ⬆️ Gửi lên máy tính

3. **Trên máy tính**:
   - Click "📱 Load Ảnh Từ Điện Thoại"
   - Ảnh sẽ tự động hiển thị
   - Click "🔍 Phát Hiện Bệnh"

### **Cách 3: Mở file trực tiếp**
```
c:\Users\Admin\Desktop\AI_Agri\index.html
(Khuyến cáo: Nên dùng Cách 1 hoặc 2 thay vì mở file trực tiếp)

---

## 📋 Hướng Dẫn Chi Tiết - Chụp Ảnh Điện Thoại

### **Bước 1: Chuẩn Bị**
- ✅ Terminal 1: Ganache (giữ chạy)
- ✅ Terminal 2: Deploy contract (chạy xong)
- ✅ Terminal 3: Flask (giữ chạy)
- ✅ Điện thoại + PC cùng WiFi

### **Bước 2: Điện Thoại - Chụp Ảnh**
1. Mở trình duyệt trên điện thoại
2. Nhập: `http://192.168.111.187:5000/phone.html` (thay IP của bạn)
3. **Cách 1: Click vào khung "📂 Click để chọn ảnh"**
   - Chọn ảnh từ thư viện **HOẶC**
   - Chụp ảnh mới trong dialog
   - ✅ **CÁCH NÀY HOẠT ĐỘNG 100%**

4. Xem trước ảnh
5. Click "⬆️ Gửi Ảnh Lên Máy Tính"
6. Đợi ✅ "Ảnh được gửi"

⚠️ **Ghi Chú**: Nút "📹 Mở Camera" có thể không hoạt động trên HTTP (lỗi bảo mật của Chrome). Dùng "Chọn Ảnh Từ Thư Viện" thay thế!

### **Bước 3: Máy Tính - Phát Hiện**
1. Mở `http://localhost:5000`
2. Click **"📱 Load Ảnh Từ Điện Thoại"**
3. Ảnh tự động hiển thị
4. Click **"🔍 Phát Hiện Bệnh"**
5. Xem kết quả + lưu lên blockchain

---

| Component | Status | Check |
|-----------|--------|-------|
| 🔗 Ganache | Port 8545 | Terminal 1 → "Listening on 127.0.0.1:8545" |
| ⛓️ Contract | Deployed | Terminal 2 → "✅ Deployed at: 0x..." |
| 🌐 Flask API | Port 5000 | Terminal 3 → "Running on http://localhost:5000" |
| 📁 HTTP Server | Port 8000 | Terminal 4 → "Serving HTTP on..." |

---

## 💡 Ghi Chú Quan Trọng

- **Terminal 1 PHẢI giữ chạy** - Đây là blockchain local
- **Terminal 2** chỉ chạy lần đầu + khi reset contract
- **Terminal 3** chứa API chính, cần giữ chạy
- **Terminal 4** là tùy chọn, không bắt buộc

---

## 🚀 Quy Trình Nhanh

```powershell
# Terminal 1
ganache --host 127.0.0.1 --port 8545 --deterministic

# Terminal 2 (sau khi Terminal 1 chạy)
cd c:\Users\Admin\Desktop\AI_Agri\blockchain
truffle migrate --network development

# Terminal 3 (sau khi Terminal 2 xong)
cd c:\Users\Admin\Desktop\AI_Agri
python app_flask.py

# Mở Browser
http://localhost:5000
```

---

## 📋 Cấu Hình Hiện Tại

```
Ganache:     127.0.0.1:8545
Flask:       localhost:5000
HTTP Server: localhost:8000 (tùy chọn)
Contract:    0x5b1869D9A4C187F2EAa108f3062412ecf0526b24
Models:      models/best.pt (YOLOv8)
Dataset:     dataset/ (train/valid/test)
```

---

## 🔧 Troubleshooting

**❌ Camera bị lỗi trên điện thoại: "undefined is not an object"**

**Nguyên nhân**: Trình duyệt HTTP không cho phép truy cập camera (chỉ HTTPS hoặc localhost)

**Giải Pháp 1: Dùng File Upload Thay Vì Camera** ⭐ **NHANH NHẤT**
1. Mở ứng dụng trên điện thoại: `http://192.168.111.55:5000`
2. **Bỏ qua nút "📱 Mở Camera"**
3. Click vào khung "📁 Click để chọn ảnh hoặc kéo thả ảnh"
4. Chọn ảnh từ **thư viện ảnh** hoặc **chụp ảnh ngay**
5. Ấn **"🔍 Phát Hiện Bệnh"**

**Giải Pháp 2: Dùng Chrome/Firefox (Có Hỗ Trợ Camera Tốt Hơn)**
- Tắt Chrome → Mở **Firefox** hoặc **Chrome Canary**
- Thử camera lại

**Giải Pháp 3: Cấp Quyền Camera Cho Trình Duyệt**
1. Mở cài đặt điện thoại → **Apps** → Tìm trình duyệt đang dùng
2. **Permissions** → **Camera** → Chọn **"Allow"**
3. Quay lại ứng dụng → Thử mở camera lại

**Giải Pháp 4: Dùng HTTPS (Nâng Cao)**
- Cài đặt SSL certificate cho Flask
- Hoặc dùng ngrok để tunnel HTTP sang HTTPS:
```powershell
# Cài đặt
npm install -g ngrok

# Chạy
ngrok http 5000

# Sẽ tạo URL như: https://abc123.ngrok.io
# Mở trên điện thoại: https://abc123.ngrok.io
```

---

**❌ Điện thoại không kết nối được đến 192.168.111.55:5000**

**Bước 1: Kiểm tra Flask có chạy không**
```powershell
# Bật PowerShell và chạy:
netstat -ano | findstr :5000

# Kết quả nên hiển thị thứ gì đó như:
# TCP  0.0.0.0:5000  0.0.0.0:0  LISTENING  12345
# Nếu KHÔNG có → Flask chưa chạy
```

**Bước 2: Kiểm tra WiFi**
- Đảm bảo PC + Điện thoại **cùng mạng WiFi**
- Thử ping từ điện thoại đến PC:
  - Mở Command Prompt trên PC: `ipconfig` → Copy IPv4
  - Điện thoại: Tải app "Ping" từ Play Store → ping IP

**Bước 3: Mở Firewall Port 5000** ⭐ **QUAN TRỌNG**

**Cách 1: Dùng Command (Nhanh nhất)**
```powershell
# Mở PowerShell ✅ RUN AS ADMINISTRATOR
netsh advfirewall firewall add rule name="Flask_5000" dir=in action=allow protocol=tcp localport=5000

# Kết quả: "Ok."
```

**Cách 2: Dùng Windows Defender Firewall GUI**
1. Bấm `Win + R` → gõ `wf.msc` → Enter
2. Click **"Inbound Rules"** → **"New Rule"** (bên phải)
3. Chọn **"Port"** → Next
4. Chọn **"TCP"** + nhập `5000` → Next
5. Chọn **"Allow the connection"** → Next
6. Chọn hết các checkbox (Domain, Private, Public) → Next
7. Tên: `Flask_5000` → Finish

**Bước 4: Restart Flask**
```powershell
# Đóng terminal Flask đang chạy
# Chạy lại:
cd c:\Users\Admin\Desktop\AI_Agri
python app_flask.py
```

**Bước 5: Test Kết Nối**
- Máy tính: `http://localhost:5000` ✅
- Điện thoại: `http://192.168.111.55:5000` ✅

---

**Tìm IP Address của máy tính (cho điện thoại)**
```powershell
# Bật PowerShell và chạy:
ipconfig

# Tìm dòng có "IPv4 Address: 192.168.x.x"
# Ví dụ: 192.168.111.55 → Nhập http://192.168.111.55:5000
```

**Port đã bị sử dụng?**
```powershell
# Tìm process sử dụng port
netstat -ano | findstr :8545
netstat -ano | findstr :5000
netstat -ano | findstr :8000

# Kill process (thay PID)
taskkill /PID [PID] /F
```

**Ganache không chạy?**
```powershell
# Cài đặt global
npm install -g ganache
```

**Flask không tìm thấy module?**
```powershell
# Cài đặt dependencies
pip install -r requirements.txt
```

---

**Happy Farming! 🌾✨**
