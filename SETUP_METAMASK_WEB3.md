# 🔗 SETUP METAMASK + WEB3 (Ganache Local)

## **Chạy Web3 App Với MetaMask**

### **Prerequisite:**
- ✅ Ganache đang chạy: `ganache --host 127.0.0.1 --port 8545 --deterministic`
- ✅ Smart contract đã deploy
- ✅ MetaMask extension đã cài đặt

---

## **BƯỚC 1: Setup MetaMask**

### **1.1 Mở MetaMask**
- Click icon MetaMask ở top-right
- Unlock wallet (nếu cần)

### **1.2 Thêm Ganache Network**

**Cách làm:**
1. Click tên network (default: "Ethereum Mainnet")
2. Scroll xuống → Click "Add Network"
3. Nhập thông tin:

```
Network Name: Ganache Local
RPC URL: http://127.0.0.1:8545
Chain ID: 1337
Currency: ETH
```

4. Click "Save"

### **1.3 Import Account từ Ganache**

**Lấy Private Key từ Ganache:**

```
Terminal Ganache sẽ hiển thị:
Available Accounts:
(0) 0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1 (1000 ETH)
Private Keys:
(0) 0x...

SAO CHÉP private key (dài 64 ký tự)
```

**Import vào MetaMask:**
1. Click avatar (top-right)
2. Select Account → Add Account
3. Chọn "Import using Private Key"
4. Paste private key từ Ganache
5. Click "Import"

---

## **BƯỚC 2: Chạy Backend Flask**

```bash
cd c:\Users\Admin\Desktop\AI_Agri

# Cài flask + flask-cors
pip install flask flask-cors

# Chạy backend
python app_flask.py
```

**Output:**
```
🚀 Flask API chạy trên http://localhost:5000
```

✅ **GIỮ CHẠY** (đừng đóng)

---

## **BƯỚC 3: Mở Web3 App**

**Cách 1: Trực tiếp file**
```
Mở file: c:\Users\Admin\Desktop\AI_Agri\index.html
Dùng trình duyệt bất kỳ
```

**Cách 2: Dùng Python HTTP server (Recommended)**
```bash
# Terminal mới
cd c:\Users\Admin\Desktop\AI_Agri

# Start HTTP server
python -m http.server 8000
```

Sau đó mở: `http://localhost:8000`

---

## **BƯỚC 4: Connect MetaMask**

1. Trên trang Web3 App
2. Click button "🔗 Connect MetaMask"
3. **MetaMask popup sẽ hiện** (tự động)
4. Click "Connect"
5. Chọn account (Ganache account)
6. Click "Next" → "Connect"

✅ **Kết nối thành công**

---

## **BƯỚC 5: Workflow Sử Dụng**

### **Phát Hiện Bệnh:**
1. Upload ảnh lá lúa
2. Click "🔍 Phát Hiện Bệnh"
3. Backend xử lý (YOLOv8 + Groq)
4. Kết quả hiển thị

### **Lưu Blockchain (MetaMask Tự Động):**
1. Click "💾 Lưu lên Blockchain"
2. **MetaMask popup TỰ ĐỘNG hiện** (khoảng 1 giây)
3. **User xác nhận trên MetaMask** (click "Confirm")
4. Transaction gửi đến Ganache
5. ✅ TX Hash + Block Number hiển thị

---

## **⚠️ TROUBLESHOOTING**

### **❌ "Cannot connect to localhost:5000"**
- ✅ Chắc chắn Flask đang chạy
- ✅ Port 5000 không bị chiếm

### **❌ "MetaMask không hiện"**
- ✅ Kiểm tra MetaMask extension (enable)
- ✅ Refresh trang web
- ✅ Restart browser

### **❌ "Ganache network không hiển thị"**
- ✅ Kiểm tra Chain ID = 1337
- ✅ Kiểm tra RPC URL = 127.0.0.1:8545

### **❌ "Transaction rejected"**
- ✅ Kiểm tra account có đủ ETH (mất gas fee)
- ✅ Kiểm tra smart contract address đúng
- ✅ Kiểm tra Ganache còn chạy không

### **❌ "CORS error"**
- ✅ Flask-CORS đã cài `pip install flask-cors`
- ✅ Flask đang chạy trên port 5000

---

## **📊 3 TERMINAL CHẠY ĐỒNG THỜI**

```
┌─────────────────────────┐
│ Terminal 1: Ganache     │
│ ganache --host ...      │ ← CHẠY TRƯỚC
└─────────────────────────┘
         ↓
┌─────────────────────────┐
│ Terminal 2: Flask API   │
│ python app_flask.py     │ ← CHẠY THỨ 2
└─────────────────────────┘
         ↓
┌─────────────────────────┐
│ Terminal 3: HTTP Server │
│ python -m http.server   │ ← CHẠY THỨ 3
└─────────────────────────┘
         ↓
    Mở Browser
    localhost:8000
```

---

## **✅ SỰ KHÁC BIỆT SO VỚI STREAMLIT**

| Tính Năng | Streamlit | Web3 (ethers.js) |
|-----------|-----------|------------------|
| **MetaMask** | ❌ Không | ✅ Có |
| **Transaction Confirmation** | Backend xử lý | ✅ User xác nhận |
| **Frontend** | Python | HTML + JavaScript |
| **Real Web3** | Fake popup | ✅ Thật 100% |

---

## **🚀 DEMO WORKFLOW**

```
1. User upload ảnh
   ↓
2. Click "Phát Hiện Bệnh"
   ↓
   Backend (Flask):
   - YOLOv8 detect
   - Groq tư vấn
   - Lưu local
   ↓
3. Kết quả hiển thị
   ↓
4. User click "Lưu lên Blockchain"
   ↓
   Frontend (ethers.js):
   - Call smart contract
   - MetaMask popup TỰ ĐỘNG ← QUAN TRỌNG
   ↓
5. 🔴 MetaMask popup hiển thị
   - User thấy transaction details
   - User click "Confirm"
   ↓
6. Ganache nhận transaction
   ↓
7. ✅ TX Hash + Block Number
   ↓
8. Frontend cập nhật UI
```

---

## **📝 NOTES**

- MetaMask **chỉ dùng để ký transaction**
- **Backend vẫn xử lý YOLOv8 + Groq**
- **Data vẫn lưu local + blockchain**
- **Có thể chạy Streamlit + Web3 cùng lúc** (port khác nhau)

---

**Bắt đầu thôi! 🚀**
