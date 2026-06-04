# ⚡ QUICK START - BLOCKCHAIN CHO AI_AGRI

## 🎯 Kế hoạch 3 bước nhanh chóng

### **BƯỚC 1: CÀI ĐẶT (5 phút)**

#### 1.1 Cài Ganache Global
```powershell
npm install -g ganache
```

#### 1.2 Cài Web3.py
```powershell
pip install web3
```

#### 1.3 Cài Truffle & Dependencies (trong folder blockchain)
```powershell
cd c:\Users\Admin\Desktop\AI_Agri\blockchain
npm install
```

---

### **BƯỚC 2: START BLOCKCHAIN (30 giây)**

**Terminal #1 - Chạy Ganache:**
```powershell
ganache --host 127.0.0.1 --port 8545 --deterministic
```

Giữ cửa sổ này mở! Output sẽ hiển thị:
```
Available Accounts
==================
(0) 0x1234567890...
(1) 0xabcdef...
...
Listening on 127.0.0.1:8545
```

---

### **BƯỚC 3: DEPLOY CONTRACT (2 phút)**

**Terminal #2 - Compile & Deploy:**
```powershell
cd c:\Users\Admin\Desktop\AI_Agri\blockchain

# Compile
truffle compile (không cần chạy lần thứ 2)

# Deploy
truffle migrate --network development
```

**Output mong đợi:**
```
> contract address:    0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
```

⭐ **GHI LẠI ADDRESS này!**

---

### **BƯỚC 4: CẬP NHẬT APP.PY**

Mở `c:\Users\Admin\Desktop\AI_Agri\blockchain_service.py`

Tìm dòng này ở hàm `init_blockchain()`:
```python
bs.contract_address = "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0"  # ← THAY ĐỔI
```

Thay bằng contract address từ bước 3!

---

### **BƯỚC 5: CHẠY APP (30 giây)**

**Terminal #3 - Streamlit:**
```powershell
cd c:\Users\Admin\Desktop\AI_Agri
pip install -r requirements.txt  # Lần đầu chạy
streamlit run app.py
```

Trình duyệt sẽ mở: `http://localhost:8501`

---

## 📊 HỘI TỤ HOÀN CHỈNH

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Terminal #1   │     │   Terminal #2    │     │   Terminal #3   │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│   Ganache       │     │  Truffle         │     │  Streamlit      │
│   (đang chạy)   │     │  (deploy)        │     │  (app.py)       │
│ :8545          │     │  ✅ hoàn thành    │     │ :8501           │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        ↓                        ↓                        ↓
   Blockchain           Smart Contract          Web Interface
   (Local)              (Deployed)              (User Access)
```

---

## 🧪 TEST BLOCKCHAIN (Không cần Streamlit)

Để test mà không dùng Streamlit:

```powershell
cd c:\Users\Admin\Desktop\AI_Agri
python blockchain_example.py
```

Output sẽ hiển thị:
```
✅ Account: 0x1234567890...
💰 Balance: 100 ETH
✅ Contract loaded: 0x9fE46...

TEST 1: TẠO RECORD BỆNH MỚI
✅ Lưu thành công!
   TX Hash: 0xabc123...
   Block: 2

TEST 2: LẤY THÔNG TIN RECORD
✅ Record ID: 0
   Diseases: ['Bệnh Đốm nâu', 'Bệnh Bạc lá']
...
```

---

## 🐛 QUICK FIX

| Vấn đề | Giải pháp |
|-------|----------|
| `Cannot connect to 127.0.0.1:8545` | ✅ Mở cửa sổ Ganache |
| `Contract not found` | ✅ Chạy `truffle migrate --reset` |
| `Module 'web3' not found` | ✅ `pip install web3` |
| Ganache tạo blockchain mới | ✅ Bắt đầu lại migration |

---

## 📱 WORKFLOW THỰC TẾ

```
1️⃣  Upload ảnh bệnh lúa
    ↓
2️⃣  YOLOv8 phát hiện bệnh
    ↓
3️⃣  Groq AI tư vấn
    ↓
4️⃣  Click "Lưu kết quả"
    ├─ Lưu JSON local (history/data.json)
    └─ Lưu Blockchain (RiceDiseaseRecord.sol)
    ↓
5️⃣  Xem lịch sử
    ├─ Thông tin local
    └─ TX Hash & Block Number từ blockchain
```

---

## 🎓 ĐIỀU GÌ ĐƯỢC LƯU TRÊN BLOCKCHAIN?

```json
{
  "id": 0,
  "farmer": "0x1234567890...",
  "imageHash": "abc123def456...",
  "diseases": ["Bệnh Đốm nâu"],
  "medications": ["Azoxystrobin", "Tebuconazole"],
  "advice": "Phun thuốc mỗi 7-10 ngày...",
  "timestamp": 1715002800,  // Unix timestamp
  "temperature": "28°C",
  "humidity": "75%"
}
```

**Tất cả được lưu VĨNH VIỄN trên blockchain!** ✅

---

## 💡 TẬT CẢ CÔNG CỤ CẬN THIẾT

| Tool | Dùng cho | Status |
|------|----------|--------|
| **Ganache** | Local blockchain | ✅ Cài rồi |
| **Truffle** | Deploy contract | ✅ Cài rồi |
| **Web3.py** | Kết nối Python ↔ Blockchain | ✅ Cài rồi |
| **Streamlit** | Web UI | ✅ Cài rồi |
| **YOLOv8** | Detect bệnh | ✅ Cài rồi |
| **Groq** | AI tư vấn | ✅ API key cài rồi |

---

## 🎉 HOÀN THÀNH!

Bây giờ mỗi khi lưu bệnh lúa:
✅ Lưu local (JSON + ảnh)  
✅ Lưu blockchain (smart contract)  
✅ Nhận TX hash & block number  

**Dữ liệu VĨNH VIỄN & BẤT BIẾN!** 🚀

---

## 📚 DOCS CHI TIẾT

- **Blockchain Setup:** `BLOCKCHAIN_SETUP.md`
- **Smart Contract:** `blockchain/contracts/RiceDiseaseRecord.sol`
- **BlockchainService API:** `blockchain_service.py`
- **Example Code:** `blockchain_example.py`
