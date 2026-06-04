# 🌾 AI_Agri - Rice Disease Detection with AI & Blockchain

**Hệ thống phát hiện bệnh lúa tự động kết hợp YOLOv8 AI, Groq LLM và Smart Contract trên Blockchain**

---

## 🎯 Tính Năng Chính

✅ **Phát hiện bệnh lúa** - YOLOv8 Deep Learning với bounding boxes  
✅ **Tư vấn điều trị** - Groq AI cung cấp lời khuyên tiếng Việt  
✅ **Lưu trữ blockchain** - Smart Contract (Solidity) trên Ganache  
✅ **Lịch sử đầy đủ** - JSON local + blockchain records  
✅ **Email notifications** - Cảnh báo tự động  
✅ **Web interface** - Flask API + HTML5  

---

## 🍚 5 Loại Bệnh Lúa Được Phát Hiện

| # | Tên Bệnh | Tên Khoa Học | Triệu Chứng |
|----|----------|-------------|-----------|
| 1 | **Bệnh Bạc lá** | *Xanthomonas oryzae* | Lá vàng → bạc, mềm, ẩm |
| 2 | **Bệnh Đốm nâu** | *Helminthosporium oryzae* | Đốm nâu hình bầu dục trên lá |
| 3 | **Bệnh Đạo ôn** | *Rhizoctonia solani* | Vệt khô từ lá non → lá già |
| 4 | **Bệnh Khô vằn** | *Fusarium/Pyricularia* | Vằn khô vàng/nâu trên lá |
| 5 | **Bệnh Lá Khỏe** | - | Không có dấu hiệu bệnh |

---

<div align="center">
  <img src="poster.jpg" alt="Poster" width="250">
</div>

## 🚀 Quick Start (4 Bước)

### **Terminal 1: Ganache**
```powershell
ganache --host 127.0.0.1 --port 8545 --deterministic
```

### **Terminal 2: Deploy Contract**
```powershell
cd c:\Users\Admin\Desktop\AI_Agri\blockchain
truffle migrate --network development
```

### **Terminal 3: Flask API**
```powershell
cd c:\Users\Admin\Desktop\AI_Agri
python app_flask.py
```

### **Mở Ứng Dụng**
```
http://localhost:5000
```

📖 Chi tiết: [RUN_COMMANDS.md](RUN_COMMANDS.md)

---

## 📁 Cấu Trúc Dự Án

```
AI_Agri/
├── app_flask.py              # Flask API (port 5000) ⭐
├── app.py                    # Streamlit app
├── blockchain_service.py     # Web3 integration
├── index.html               # Web3 interface
├── requirements.txt
├── models/
│   └── best.pt              # YOLOv8 model
├── blockchain/
│   ├── contracts/
│   │   └── RiceDiseaseRecord.sol
│   ├── migrations/
│   ├── truffle-config.js
│   └── package.json
├── dataset/                 # Train/valid/test
├── history/
│   ├── data.json           # Records history
│   └── images/
└── README.md
```

---

## 🛠️ Công Nghệ

**Backend:**
- Flask (API Server)
- YOLOv8 (Object Detection)
- Groq API (LLM - Llama 3.3-70B)
- Web3.py (Blockchain)

**Frontend:**
- HTML5 + JavaScript (ethers.js)
- Streamlit (Alternative UI)

**Blockchain:**
- Solidity (Smart Contract)
- Ganache (Local Ethereum)
- Truffle (Deployment)

**ML/CV:**
- OpenCV
- NumPy
- Ultralytics

---

## 📋 API Endpoints

| Method | Endpoint | Mô Tả |
|--------|----------|-------|
| POST | `/api/detect` | Upload ảnh → phát hiện bệnh + bounding boxes |
| GET | `/api/history/get` | Lấy lịch sử tất cả records |
| POST | `/api/blockchain/save` | Lưu record lên blockchain |
| GET | `/api/blockchain/account` | Lấy Ganache account info |

---

## 📦 Cài Đặt Dependencies

```powershell
# Python packages
pip install -r requirements.txt

# Node packages (Blockchain)
cd blockchain
npm install
```

---

## ⚙️ Cấu Hình

**Groq API Key** - `app_flask.py` line ~30
```python
client_groq = Groq(api_key="gsk_...")
```

**Smart Contract Address** - `blockchain_service.py`
```python
self.contract_address = "0x5b1869D9A4C187F2EAa108f3062412ecf0526b24"
```

**Email Notifications** - `app_flask.py` (tùy chọn)

---

## 📊 Luồng Dữ Liệu

```
1. User Upload Image
       ↓
2. YOLOv8 Detection + Bounding Boxes
       ↓
3. Groq AI (Vietnamese Treatment Advice)
       ↓
4. Save to JSON Local + Blockchain
       ↓
5. Email Notification (if enabled)
       ↓
6. Display Results + History
```

---

## 🔐 Blockchain Features

- **Smart Contract**: Ghi lại loại bệnh, thuốc, tư vấn, timestamp
- **Record Storage**: Trên Ganache local (127.0.0.1:8545)
- **Data Integrity**: SHA-256 hash của hình ảnh
- **Transaction Hash**: Lưu TX hash + block number

---

## 📸 Kết Quả Phát Hiện

API trả về:
- ✅ Danh sách bệnh phát hiện
- ✅ Confidence scores (%)
- ✅ **Bounding boxes** (tọa độ + label)
- ✅ Ảnh annotated (base64)
- ✅ Lời khuyên tiếng Việt
- ✅ Danh sách thuốc trị

---

## 🎓 Example Response

```json
{
  "success": true,
  "diseases": ["Bệnh Đốm nâu"],
  "confidence": 0.95,
  "annotated_image_base64": "data:image/jpeg;base64,...",
  "boxes": [
    {
      "class": "Bệnh Đốm nâu",
      "confidence": 0.95,
      "coords": [100, 150, 300, 450]
    }
  ],
  "medications": ["Azoxystrobin", "Tebuconazole"],
  "advice": "Phun thuốc mỗi 7-10 ngày...",
  "tx_hash": "0x816d...",
  "block_number": 6
}
```

---

## 📞 Contact & Support

- 📧 Email: `hamy5dvdsz@gmail.com`
- 🌐 Ganache: `127.0.0.1:8545`
- 🔗 Contract: `0x5b1869D9A4C187F2EAa108f3062412ecf0526b24`

---

## 📄 License

CC BY 4.0 - Agricultural Research

---

**Happy Farming! 🌾✨**
- **Tính năng**:
  - Tìm kiếm theo loại bệnh
  - Lọc theo ngày
  - Xem chi tiết lịch sử blockchain
  - Xuất báo cáo

---

## 4. Công Nghệ Sử Dụng

### Backend
- **Python 3.8+**: Ngôn ngữ chính
- **TensorFlow 2.x**: Framework Deep Learning
- **OpenCV**: Xử lý hình ảnh
- **Streamlit**: Framework tạo web app
- **Web3.py**: Tương tác với blockchain
- **Solidity**: Viết Smart Contract

### Frontend
- **Streamlit**: Giao diện người dùng
- **HTML/CSS**: Styling
- **JavaScript**: Tương tác động

### Blockchain
- **Ethereum**: Network blockchain
- **Ganache**: Local blockchain development
- **MetaMask**: Ví điện tử
- **Truffle**: Công cụ phát triển Smart Contract

### Database
- **Smart Contract Storage**: Lưu trữ dữ liệu trên blockchain
- **JSON Files**: Lưu trữ metadata cục bộ (tùy chọn)

### Bảo Mật
- **SHA-256**: Hashing hình ảnh
- **KECCAK-256**: Hashing blockchain
- **RSA/ECDSA**: Chữ ký số

---

## 5. Hướng Dẫn Cài Đặt Chi Tiết

### 5.1 Yêu Cầu Hệ Thống
- **OS**: Windows 10/11, macOS, hoặc Linux
- **RAM**: Tối thiểu 4GB (8GB được khuyến nghị)
- **Storage**: 5GB trống cho dependencies
- **Python**: Phiên bản 3.8 hoặc cao hơn
- **Node.js**: v14 trở lên

### 5.2 Bước 1: Cài Đặt Python và Dependencies

`ash
# Cập nhật pip
python -m pip install --upgrade pip

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate
`

### 5.3 Bước 2: Clone Dự Án

`ash
git clone https://github.com/your-repo/AI_Agri.git
cd AI_Agri
`

### 5.4 Bước 3: Cài Đặt Thư Viện Python

`ash
pip install -r requirements.txt
`

Nội dung file 
equirements.txt:
`
streamlit==1.28.0
tensorflow==2.13.0
keras==2.13.0
opencv-python==4.8.0
numpy==1.24.0
pandas==2.0.0
web3==6.11.0
Pillow==10.0.0
Werkzeug==2.3.0
scikit-image==0.21.0
matplotlib==3.7.0
`

### 5.5 Bước 4: Cài Đặt Node.js và Truffle

`ash
# Cài đặt Node.js từ https://nodejs.org/

# Cài đặt Truffle
npm install -g truffle

# Cài đặt Ganache CLI
npm install -g ganache-cli
`

### 5.6 Bước 5: Cài Đặt và Cấu Hình Blockchain

`ash
# Cài đặt Ganache
npm install -g ganache

# Chạy Ganache (tạo local blockchain)
ganache --deterministic --accounts 10 --host-name localhost --port 8545
`

Thông tin kết nối:
- **RPC URL**: http://localhost:8545
- **Chain ID**: 1337
- **Accounts**: 10 tài khoản test
- **Gas Limit**: Không giới hạn

### 5.7 Bước 6: Deploy Smart Contract

`ash
# Vào thư mục blockchain
cd blockchain

# Compile contract
truffle compile

# Deploy lên Ganache
truffle migrate --network development

# Lưu lại contract address
`

### 5.8 Bước 7: Cấu Hình Ứng Dụng

Tạo file config.py trong thư mục gốc:
`python
# Blockchain Configuration
WEB3_PROVIDER = "http://localhost:8545"
CONTRACT_ADDRESS = "0x..." # Copy từ output deploy
PRIVATE_KEY = "0x..." # Lấy từ Ganache
GAS_LIMIT = 3000000
GAS_PRICE = 20

# Model Configuration
MODEL_PATH = "./models/rice_disease_model.h5"
CONFIDENCE_THRESHOLD = 0.75

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8501
`

### 5.9 Bước 8: Tải Mô Hình AI

`ash
# Mô hình pre-trained
# Tải từ link và đặt vào thư mục models/
# Hoặc huấn luyện lại mô hình:
python train_model.py
`

### 5.10 Bước 9: Chạy Ứng Dụng

`ash
# Đảm bảo Ganache đang chạy

# Chạy ứng dụng Streamlit
streamlit run app.py
`

Ứng dụng sẽ mở tại: http://localhost:8501

---

## 6. Hướng Dẫn Sử Dụng Hệ Thống

### 6.1 Giao Diện Chính
1. Mở ứng dụng tại http://localhost:8501
2. Chọn trang từ sidebar (Home, Detection, History)

### 6.2 Phát Hiện Bệnh (Detection)

**Bước 1**: Tải Hình Ảnh
- Nhấn nút "Upload Image"
- Chọn file ảnh từ máy tính (JPEG, PNG, JPG)
- Hoặc sử dụng camera để chụp ảnh trực tiếp

**Bước 2**: Xử Lý Hình Ảnh
- Ứng dụng tự động xử lý hình ảnh
- Hiển thị preview hình ảnh đã tải

**Bước 3**: Phân Loại Bệnh
- AI model phân tích hình ảnh
- Trả về kết quả dự đoán
- Hiển thị loại bệnh và độ tin cậy

**Bước 4**: Xem Kết Quả
- **Tên bệnh**: Loại bệnh được phát hiện
- **Confidence**: Mức độ tin cậy (%)
- **Image Hash**: Mã hash SHA-256 của hình ảnh
- **Mô tả**: Chi tiết về bệnh
- **Khuyến nghị**: Biện pháp phòng chống

**Bước 5**: Lưu Blockchain
- Nhấn "Save to Blockchain"
- Xác nhận transaction
- Lưu ý gas fee sẽ được trừ từ ví

### 6.3 Xem Lịch Sử (History)

- Hiển thị danh sách tất cả phát hiện
- Tìm kiếm theo loại bệnh hoặc ngày
- Nhấn vào bản ghi để xem chi tiết
- Xem transaction hash trên blockchain explorer

### 6.4 Quản Lý Ví Metamask
- Cài đặt Metamask extension
- Kết nối với Ganache network
- Import tài khoản từ Ganache
- Kiểm tra ETH balance

---

## 7. Tính Năng Blockchain và Smart Contract

### 7.1 Smart Contract - DiseaseDetectionRegistry

`solidity
contract DiseaseDetectionRegistry {
    // Struct lưu trữ thông tin phát hiện bệnh
    struct DiseaseRecord {
        uint256 id;
        address farmer;
        string imageHash;      // SHA-256 hash
        string diseaseName;
        uint8 confidence;
        string location;
        uint256 timestamp;
        bool verified;
    }

    // Mapping để lưu trữ records
    mapping(uint256 => DiseaseRecord) public records;
    mapping(address => uint256[]) public userRecords;
    
    // Events
    event DiseaseDetected(
        uint256 indexed recordId,
        address indexed farmer,
        string imageHash,
        string diseaseName
    );


### 7.2 Quy Trình Lưu Blockchain

1. **Tính Hash Hình Ảnh**
   - Đọc file hình ảnh
   - Tính SHA-256 hash
   - Lưu hash 64 ký tự

2. **Gọi Smart Contract**
   - Gọi hàm 
ecordDisease()
   - Gửi imageHash, diseaseName, confidence
   - Ký transaction bằng private key

3. **Xác Nhận Transaction**
   - Ganache xác nhận transaction
   - Lưu vào block mới
   - Trả về transaction hash

4. **Lưu Metadata Cục Bộ**
   - Lưu transaction hash
   - Lưu timestamp
   - Lưu farm location

### 7.3 Lợi Ích của Blockchain

- **Tính Minh Bạch**: Tất cả phát hiện ghi lại công khai
- **Tính Bất Biến**: Dữ liệu không thể thay đổi
- **Theo Dõi Đầu Đủ**: Lịch sử lâu dài
- **Xác Thực Hình Ảnh**: Hash đảm bảo không giả mạo
- **Phi Tập Trung**: Không cần máy chủ trung tâm

---

## 8. Giải Thích về Image Hash

### 8.1 Hash là Gì?

Hash là một hàm toán học tạo ra một chuỗi ký tự dài từ dữ liệu đầu vào:

`
Hình ảnh (Đầu vào) → SHA-256 Hash (Đầu ra)
size: 2MB          → 64 ký tự hex
`

### 8.2 SHA-256

- **Kích thước output**: 256 bit = 64 ký tự hexadecimal
- **Tính chất**:
  - Một chiều (không thể reverse)
  - Deterministic (cùng input → cùng output)
  - Collision-free (gần như không thể hai ảnh khác có hash giống)

### 8.3 Ví Dụ

`
Ảnh lúa bệnh 1.jpg:
SHA-256: 7d1a4e8c2f9b3e6a1c5d8f2b9e4a7c3f5d8a1e6c9b2f4a7d0e3f6a9c2e5b8

Ảnh lúa bệnh 1.jpg (sau thay đổi 1 pixel):
SHA-256: a9f2c4e8b6d3a1f5c7e9a2d4f6b8c0e2a4d6f8a0c2e4f6a8c0e2f4a6c8d0e
`

### 8.4 Ứng Dụng trong Hệ Thống

**Xác Minh Tính Toàn Vẹn**:
`
Lần 1: Tải ảnh lên → Tính hash A
Lần 2: Tải ảnh xuống → Tính hash B
Nếu A == B → Ảnh không bị thay đổi ✓
`

**Phát Hiện Giả Mạo**:
`
Nếu ai đó thay đổi ảnh:
Hash cũ ≠ Hash mới → Phát hiện giả mạo ✗
`

**Lưu Trữ Hiệu Quả**:
`
Thay vì lưu ảnh (2MB) → Lưu hash (64 byte)
Tiết kiệm: 99.9% không gian
`

---

## 9. Biện Pháp Bảo Mật

### 9.1 Bảo Mật Hình Ảnh

- **Validate input**: Kiểm tra định dạng, kích thước
- **Scan virus**: Quét file trước khi xử lý
- **Lưu trữ an toàn**: Mã hóa hình ảnh khi lưu
- **Hash verification**: Xác minh hash trước xử lý

### 9.2 Bảo Mật Blockchain

`python
# Không bao giờ hardcode private key
# Sử dụng environment variables
private_key = os.environ.get("PRIVATE_KEY")

# Xác minh địa chỉ sender
require(msg.sender == recordOwner, "Only record owner can verify")

# Kiểm tra gas price
require(tx.gasprice <= MAX_GAS_PRICE, "Gas price too high")
`

### 9.3 Bảo Mật Ứng Dụng

- **HTTPS**: Mã hóa kết nối
- **Authentication**: Xác thực người dùng
- **Authorization**: Phân quyền truy cập
- **Input Validation**: Kiểm tra tất cả input
- **SQL Injection**: Tránh query tương tác

### 9.4 Bảo Mật Mô Hình AI

- **Model obfuscation**: Che giấu model
- **Prediction logging**: Ghi lại dự đoán
- **Adversarial defense**: Phòng chống tấn công
- **Regular updates**: Cập nhật model định kỳ

### 9.5 Danh Sách Kiểm Tra Bảo Mật

- [ ] Cài đặt HTTPS
- [ ] Bảo vệ private key
- [ ] Kiểm tra input
- [ ] Cập nhật dependencies
- [ ] Sử dụng environment variables
- [ ] Logging và monitoring
- [ ] Backup dữ liệu
- [ ] Rate limiting API

---

## 10. Hướng Dẫn Khắc Phục Sự Cố

### 10.1 Lỗi Khi Khởi Động

**Lỗi 1: ModuleNotFoundError: No module named 'streamlit'**
`ash
# Giải pháp:
pip install streamlit
# Hoặc cài đặt lại tất cả:
pip install -r requirements.txt
`

**Lỗi 2: Port 8501 already in use**
`ash
# Giải pháp 1: Dùng port khác
streamlit run app.py --server.port 8502

# Giải pháp 2: Tìm và kill process
netstat -ano | findstr :8501
taskkill /PID <PID> /F
`

**Lỗi 3: Python version not compatible**
`ash
# Kiểm tra version
python --version

# Cần Python 3.8+
# Tải từ python.org
`

### 10.2 Lỗi Blockchain

**Lỗi 4: Unable to connect to http://localhost:8545**
`ash
# Kiểm tra Ganache đang chạy
# Mở terminal mới, chạy:
ganache

# Hoặc sử dụng Ganache GUI
`

**Lỗi 5: Contract address is invalid**
`ash
# Kiểm tra config.py
# Đảm bảo CONTRACT_ADDRESS đúng
# Chạy deploy lại:
cd blockchain
truffle migrate --network development --reset
`

**Lỗi 6: Insufficient funds**
`ash
# Kiểm tra balance ví
web3.eth.get_balance(account)

# Request faucet test ETH hoặc import tài khoản Ganache
`

### 10.3 Lỗi AI Model

**Lỗi 7: Model file not found**
`ash
# Kiểm tra đường dẫn model
# model_path trong config.py
# Đặt file model đúng vị trí:
AI_Agri/models/rice_disease_model.h5
`

**Lỗi 8: Out of memory when loading model**
`ash
# Giải pháp:
# 1. Tăng RAM
# 2. Sử dụng model nhỏ hơn
# 3. Load model theo yêu cầu

# Code:
@st.cache_resource
def load_model():
    return load_trained_model("models/rice_disease_model.h5")
`

**Lỗi 9: Prediction accuracy low**
`ash
# Kiểm tra:
# - Chất lượng ảnh đầu vào
# - Ánh sáng đủ
# - Nền sạch
# - Hình ảnh rõ ràng

# Huấn luyện lại model:
python train_model.py --epochs 50 --batch-size 32

## 12. Tài Liệu Tham Khảo và Liên Kết Hữu Ích

### Tài Liệu Chính Thức
- **Streamlit Documentation**: https://docs.streamlit.io
- **TensorFlow Documentation**: https://www.tensorflow.org/
- **Web3.py Documentation**: https://web3py.readthedocs.io
- **Solidity Documentation**: https://docs.soliditylang.org

### Hướng Dẫn Blockchain
- **Ethereum Official**: https://ethereum.org/en/developers/
- **Ganache**: https://www.trufflesuite.com/ganache
- **MetaMask**: https://metamask.io/
- **Remix IDE**: https://remix.ethereum.org/

### Tài Nguyên Nông Nghiệp
- **FAO Rice Diseases**: http://www.fao.org/
- **Công Bố Nghiên Cứu**: Springer, IEEE Xplore
- **Các Giống Lúa Kháng**: IRRI (International Rice Research Institute)

---

## 13. Liên Hệ và Hỗ Trợ

- **Email**: support@ai-agri.dev
- **GitHub Issues**: https://github.com/your-repo/issues
- **Community Forum**: https://forum.ai-agri.dev
- **Hotline Hỗ Trợ**: +84-xxx-xxx-xxxx (Giờ hành chính)

---

## 14. Giấy Phép

Dự án AI_Agri được phát hành dưới giấy phép MIT. Xem file LICENSE để chi tiết.

---

## 15. Lời Cảm Ơn

Cảm ơn các cá nhân và tổ chức đã hỗ trợ dự án:
- IRRI (International Rice Research Institute)
- Bộ Nông Nghiệp & Phát Triển Nông Thôn
- Các nhà nông trong cộng đồng
- Đóng góp từ cộng đồng mã nguồn mở

---

**Phiên bản**: 1.0  
**Cập nhật lần cuối**: 2024  
**Tác giả**: AI_Agri Development Team  
**Ngôn ngữ**: Tiếng Việt

---

© 2024 AI_Agri. All rights reserved.
