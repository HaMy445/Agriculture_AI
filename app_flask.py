"""
Flask Backend API cho AI_Agri Web3 App
- YOLOv8 phát hiện bệnh
- Groq LLM tư vấn
- Web3 blockchain integration
- Email notifications
- Local history management
"""

from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import io
import hashlib
import json
import os
from datetime import datetime
from blockchain_service import BlockchainService
import smtplib
from email.mime.text import MIMEText
import base64
import numpy as np
import cv2

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# --- KHỞI TẠO ---
GROQ_API_KEY = ""
client_groq = Groq(api_key=GROQ_API_KEY)

# Blockchain service
try:
    blockchain_service = BlockchainService(provider_url="http://127.0.0.1:8545")
except Exception as e:
    print(f"⚠️ Blockchain khởi tạo lỗi: {e}")
    blockchain_service = None

# Tạo thư mục
HISTORY_DIR = "history"
IMAGE_DIR = os.path.join(HISTORY_DIR, "images")
PHONE_UPLOAD_DIR = os.path.join(HISTORY_DIR, "phone_uploads")
DATA_FILE = os.path.join(HISTORY_DIR, "data.json")
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(PHONE_UPLOAD_DIR, exist_ok=True)

# Model
model = YOLO("models/best.pt")

# Từ điển
vi_labels = {
    'Bacterial Leaf Blight': 'Bệnh Bạc lá (Vi khuẩn)',
    'Brown Spot': 'Bệnh Đốm nâu',
    'Healthy Leaf': 'Lá khỏe mạnh',
    'Leaf Blast Disease': 'Bệnh Đạo ôn (Cháy lá)',
    'Sheath Blight': 'Bệnh Khô vằn'
}

# --- HÀM HELPER ---
def get_treatment_advice(disease_name_vi):
    """Gọi Groq tư vấn"""
    prompt = f"Bạn là chuyên gia nông nghiệp VN. Hãy tư vấn điều trị bệnh '{disease_name_vi}' trên lúa ngắn gọn, có thuốc đặc trị. Nếu là lá khỏe mạnh thì trả lời 'Lá khỏe mạnh, không cần điều trị, chỉ đưa ra phương pháp chăm sóc tốt hơn'."
    try:
        chat_completion = client_groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Lỗi: {str(e)}"

def extract_medications(advice_text):
    """Extract danh sách thuốc từ advice text"""
    medications = []
    lines = advice_text.split('\n')
    
    # Tìm section về thuốc
    in_drug_section = False
    for line in lines:
        # Tìm dòng chứa "Sử dụng" + "thuốc" hoặc "Thuốc"
        if ('Sử dụng' in line or 'Thuốc' in line) and 'thuốc' in line.lower():
            in_drug_section = True
            continue
        
        # Nếu gặp section khác, thoát
        if in_drug_section and line.strip() and not any(c in line for c in ['-', '*', ':', '(']):
            # Kiểm tra nếu là đầu section mới (không chứa dấu phân tích)
            if line.startswith(('*', '-', '1.', '2.', '3.')) == False and ':' not in line:
                in_drug_section = False
        
        # Extract từ dòng bắt đầu với "-" hoặc "*"
        if (line.strip().startswith('-') or line.strip().startswith('*')):
            text = line.strip().lstrip('-*').strip()
            
            # Tách phần trước số hoặc dấu ngoặc để lấy tên thuốc
            # Ví dụ: "Azoxystrobin 250SC" → "Azoxystrobin"
            # Hoặc: "Azoxystrobin 25% SC" → "Azoxystrobin"
            if text:
                # Tìm từ đầu tiên (có thể là tên thuốc)
                words = text.split()
                if words:
                    # Lấy 1-2 từ đầu tiên làm tên thuốc
                    drug_name = words[0]
                    # Nếu từ thứ 2 không phải số, thêm vào
                    if len(words) > 1 and not words[1][0].isdigit():
                        drug_name = f"{words[0]} {words[1]}"
                    
                    if drug_name and len(drug_name) > 2 and drug_name not in medications:
                        medications.append(drug_name)
    
    # Nếu không tìm được từ dòng "-", tìm từ text "như ... , ... , ..."
    if not medications:
        for line in lines:
            if 'như' in line.lower():
                # Tách từ "như" đến hết
                if 'như' in line:
                    parts = line.split('như')[1]
                    # Tìm tên thuốc cách nhau bằng dấu phẩy hoặc "hoặc"
                    # Đầu tiên split bằng "hoặc" để tách phần
                    drug_candidates = parts.replace(' hoặc ', ',').split(',')
                    for drug in drug_candidates:
                        drug = drug.strip().rstrip('.:-)(')
                        if drug:
                            # Lấy từ đầu tiên
                            words = drug.split()
                            if words:
                                drug_name = words[0]
                                # Skip các từ chung chung
                                if drug_name not in ['là', 'được', 'có', 'giúp', 'và', 'hay', 'hoặc'] and len(drug_name) > 2:
                                    if drug_name not in medications:
                                        medications.append(drug_name)
    
    # Giới hạn tối đa 5 thuốc
    return medications[:5]

def send_email_notification(diseases, advice_text):
    """Gửi email cảnh báo"""
    sender_email = "wuveil215@gmail.com"
    receiver_email = "hamy572002@gmail.com"
    app_password = "kkeu aaum yikq zqlo"
    
    if not receiver_email or "@" not in receiver_email or receiver_email.startswith("("):
        return False
    
    try:
        content = f"Hệ thống AI Agri DNU phát hiện: {', '.join(diseases)}\n\nTư vấn: {advice_text[:200]}"
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = "🚨 CẢNH BÁO BỆNH LÚA - DNU AI"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"ℹ️ Email không gửi được: {e}")
        return False

def save_to_history(timestamp, diseases, image_path, image_hash, advice, medications=None, blockchain_result=None, tx_hash=None, block_number=None):
    """Lưu record vào history JSON"""
    try:
        history_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        
        new_entry = {
            "id": timestamp,
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "diseases": diseases,
            "medications": medications or [],
            "image_path": image_path,
            "image_hash": image_hash,
            "advice": advice,
            "blockchain_status": "confirmed" if (blockchain_result or tx_hash) else "pending"
        }
        
        # Nếu có blockchain_result từ Flask API
        if blockchain_result:
            new_entry["tx_hash"] = blockchain_result.get('tx_hash')
            new_entry["block_number"] = blockchain_result.get('block_number')
        
        # Nếu có tx_hash & block_number từ frontend (MetaMask)
        if tx_hash:
            new_entry["tx_hash"] = tx_hash
        if block_number:
            new_entry["block_number"] = block_number
        
        history_data.insert(0, new_entry)
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"❌ Lỗi lưu history: {e}")
        return False

@app.route('/')
def index():
    """Phục vụ trang index.html"""
    return send_file('index.html')

# --- API ENDPOINTS ---

@app.route('/api/health', methods=['GET'])
def health_check():
    """Kiểm tra API sống"""
    return jsonify({
        "status": "OK",
        "blockchain": blockchain_service is not None,
        "contract_address": "0x5b1869D9A4C187F2EAa108f3062412ecf0526b24"
    })

@app.route('/api/detect', methods=['POST'])
def detect_disease():
    """
    Phát hiện bệnh từ ảnh (có vẽ bounding box)
    Input: image (file)
    Output: diseases, advice, image_hash, image_path, annotated_image (base64)
    """
    try:
        # Nhận ảnh
        if 'image' not in request.files:
            return jsonify({"error": "Không có ảnh"}), 400
        
        file = request.files['image']
        image_bytes = file.read()
        image_pil = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image_np = np.array(image_pil)
        
        # Lưu ảnh gốc
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_filename = f"rice_{timestamp}.jpg"
        img_path = os.path.join(IMAGE_DIR, img_filename)
        image_pil.save(img_path)
        
        # Hash ảnh
        image_hash = hashlib.sha256(image_bytes).hexdigest()[:32]
        
        # YOLOv8 detect
        results = model.predict(image_pil, conf=0.5, imgsz=640)
        
        # Xử lý kết quả
        diseases = []
        boxes_info = []
        
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                class_id = int(box.cls[0])
                conf = float(box.conf[0])
                eng_name = results[0].names[class_id]
                vi_name = vi_labels.get(eng_name, eng_name)
                
                if vi_name not in diseases:
                    diseases.append(vi_name)
                
                # Lấy tọa độ bbox (x1, y1, x2, y2)
                xyxy = box.xyxy[0].cpu().numpy()
                boxes_info.append({
                    "class": vi_name,
                    "confidence": conf,
                    "coords": [int(x) for x in xyxy]
                })
        else:
            diseases = ["Lá khỏe mạnh"]
        
        # ⭐ VẼ BOUNDING BOXES TRÊN ẢNH (DÙNG PIL CHO TIẾNG VIỆT)
        # Chuyển numpy array → PIL Image
        annotated_pil = Image.fromarray(image_np.astype('uint8'), 'RGB')
        draw = ImageDraw.Draw(annotated_pil)
        
        # Load font tiếng Việt (tự động tìm font system)
        try:
            # Thử load font từ Windows
            font_path = "C:\\Windows\\Fonts\\arial.ttf"
            font_size = 16
            font_object = ImageFont.truetype(font_path, font_size)
        except:
            # Fallback nếu không tìm được font
            font_object = ImageFont.load_default()
        
        colors = {
            'Bệnh Bạc lá (Vi khuẩn)': (0, 255, 0),      # Green (BGR)
            'Bệnh Đốm nâu': (255, 0, 0),                 # Blue
            'Bệnh Đạo ôn (Cháy lá)': (0, 0, 255),       # Red
            'Bệnh Khô vằn': (255, 255, 0),              # Cyan
            'Lá khỏe mạnh': (0, 255, 255)               # Yellow
        }
        
        for box_data in boxes_info:
            x1, y1, x2, y2 = box_data["coords"]
            class_name = box_data["class"]
            conf = box_data["confidence"]
            color_bgr = colors.get(class_name, (0, 255, 0))
            
            # Convert BGR → RGB cho PIL
            color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0])
            
            # Vẽ bounding box
            draw.rectangle([x1, y1, x2, y2], outline=color_rgb, width=2)
            
            # Vẽ label + confidence
            label = f"{class_name} ({conf:.2f})"
            
            # Vị trí text
            text_x = x1
            text_y = y1 - 25 if y1 > 30 else y2 + 5
            
            # Vẽ background cho text (hộp màu)
            bbox = draw.textbbox((text_x, text_y), label, font=font_object)
            padding = 5
            draw.rectangle(
                [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
                fill=color_rgb
            )
            
            # Vẽ text (màu đen)
            draw.text((text_x, text_y), label, fill=(0, 0, 0), font=font_object)
        
        # Lưu ảnh annotated
        annotated_filename = f"rice_annotated_{timestamp}.jpg"
        annotated_path = os.path.join(IMAGE_DIR, annotated_filename)
        annotated_pil.save(annotated_path, quality=95)
        
        # Convert ảnh annotated thành base64 để trả về
        buffer = io.BytesIO()
        annotated_pil.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Groq tư vấn
        advice_content = ""
        for disease in diseases:
            advice = get_treatment_advice(disease)
            advice_content += f"{disease}: {advice}\n"
        
        # Extract medications từ advice text
        medications = extract_medications(advice_content)
        if not medications:
            medications = []
        
        # Gửi email tự động (nếu không phải lá khỏe mạnh)
        if diseases != ["Lá khỏe mạnh"]:
            send_email_notification(diseases, advice_content)
        
        # Lưu record vào history (chờ blockchain update sau)
        save_to_history(timestamp, diseases, f"/history/images/{img_filename}", image_hash, advice_content, medications=medications)
        
        return jsonify({
            "success": True,
            "diseases": diseases,
            "advice": advice_content,
            "medications": medications,
            "image_hash": image_hash,
            "image_path": f"/history/images/{img_filename}",
            "annotated_image_path": f"/history/images/{annotated_filename}",
            "annotated_image_base64": f"data:image/jpeg;base64,{image_base64}",
            "boxes": boxes_info,
            "timestamp": timestamp
        })
    
    except Exception as e:
        import traceback
        print(f"❌ Lỗi detect: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/blockchain/save', methods=['POST'])
def save_to_blockchain():
    """
    Lưu record lên blockchain qua web3
    Input: image_hash, diseases, medications, advice, timestamp
    Output: tx_hash, block_number
    """
    try:
        data = request.json
        image_hash = data.get('imageHash')
        diseases = data.get('diseases', [])
        medications = data.get('medications', [])
        advice = data.get('advice', '')
        timestamp = data.get('timestamp', '')
        
        if not blockchain_service:
            return jsonify({"error": "Blockchain không sẵn sàng"}), 500
        
        # Gọi blockchain service
        result = blockchain_service.save_disease_record(
            image_hash=image_hash,
            diseases=diseases,
            medications=medications[:3],
            advice=advice[:500],
            temperature="",
            humidity=""
        )
        
        if result:
            # Lưu vào history với blockchain info
            image_path = data.get('imagePath', '')
            medications = data.get('medications', [])
            save_to_history(timestamp, diseases, image_path, image_hash, advice, medications=medications, blockchain_result=result)
            
            return jsonify({
                "success": True,
                "tx_hash": result['tx_hash'],
                "block_number": result['block_number'],
                "message": "✅ Dữ liệu đã lưu lên blockchain"
            })
        else:
            return jsonify({"error": "Lưu blockchain thất bại"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/get', methods=['GET'])
def get_history():
    """Lấy tất cả lịch sử"""
    try:
        history_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        
        return jsonify({
            "success": True,
            "records": history_data,
            "total": len(history_data)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/save-local', methods=['POST'])
def save_local_history():
    """Cập nhật record với blockchain info (từ MetaMask transaction)"""
    try:
        data = request.json
        timestamp = data.get('timestamp')
        tx_hash = data.get('tx_hash', None)
        block_number = data.get('block_number', None)
        medications = data.get('medications', [])
        
        # Đọc history
        history_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        
        # Tìm record với timestamp này và update nó
        updated = False
        for record in history_data:
            if record.get('id') == timestamp:
                # Update record cũ với blockchain info
                record["blockchain_status"] = "confirmed"
                if tx_hash:
                    record["tx_hash"] = tx_hash
                if block_number:
                    record["block_number"] = block_number
                if medications:
                    record["medications"] = medications
                updated = True
                print(f"✅ Updated record {timestamp} with tx_hash: {tx_hash}")
                break
        
        # Nếu không tìm thấy, tạo record mới (fallback)
        if not updated:
            diseases = data.get('diseases', [])
            image_path = data.get('imagePath', '')
            image_hash = data.get('imageHash', '')
            advice = data.get('advice', '')
            
            new_entry = {
                "id": timestamp,
                "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "diseases": diseases,
                "medications": medications,
                "image_path": image_path,
                "image_hash": image_hash,
                "advice": advice,
                "blockchain_status": "confirmed"
            }
            
            if tx_hash:
                new_entry["tx_hash"] = tx_hash
            if block_number:
                new_entry["block_number"] = block_number
            
            history_data.insert(0, new_entry)
            print(f"⚠️ Created new record {timestamp}")
        
        # Lưu file
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)
        
        return jsonify({
            "success": True,
            "message": "✅ Cập nhật blockchain info thành công",
            "tx_hash": tx_hash,
            "block_number": block_number
        })
    except Exception as e:
        print(f"❌ Lỗi save_local_history: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/blockchain/account', methods=['GET'])
def get_account():
    """Lấy account Ganache"""
    try:
        if not blockchain_service:
            return jsonify({"error": "Blockchain không sẵn sàng"}), 500
        
        account = blockchain_service.get_default_account()
        balance = blockchain_service.get_balance(account) if account else None
        
        return jsonify({
            "account": account,
            "balance": str(balance) if balance else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/blockchain/records', methods=['GET'])
def get_records():
    """Lấy tất cả records từ blockchain"""
    try:
        if not blockchain_service:
            return jsonify({"error": "Blockchain không sẵn sàng"}), 500
        
        account = blockchain_service.get_default_account()
        records = blockchain_service.get_farmer_records_details(account)
        
        return jsonify({
            "success": True,
            "records": records if records else [],
            "total": len(records) if records else 0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== ĐIỆN THOẠI UPLOAD =====
@app.route('/api/phone/upload', methods=['POST'])
def phone_upload():
    """Điện thoại upload ảnh"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Không có ảnh"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "File trống"}), 400
        
        # Lưu ảnh vào phone_uploads
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"phone_{timestamp}.jpg"
        filepath = os.path.join(PHONE_UPLOAD_DIR, filename)
        
        img = Image.open(file.stream)
        img = img.convert('RGB')
        img.save(filepath, 'JPEG')
        
        return jsonify({
            "success": True,
            "message": "✅ Ảnh được nhận từ điện thoại!",
            "filename": filename,
            "timestamp": timestamp
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/phone/get-latest', methods=['GET'])
def phone_get_latest():
    """Máy tính lấy ảnh mới nhất từ điện thoại"""
    try:
        files = os.listdir(PHONE_UPLOAD_DIR)
        
        if not files:
            return jsonify({"success": False, "message": "Chưa có ảnh từ điện thoại"}), 404
        
        # Lấy file mới nhất
        latest_file = sorted(files)[-1]
        filepath = os.path.join(PHONE_UPLOAD_DIR, latest_file)
        
        # Convert to base64
        with open(filepath, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        return jsonify({
            "success": True,
            "image_base64": image_base64,
            "filename": latest_file
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== EMAIL =====
def send_email():
    """Gửi email thủ công"""
    try:
        data = request.json
        diseases = data.get('diseases', [])
        advice = data.get('advice', '')
        
        result = send_email_notification(diseases, advice)
        
        return jsonify({
            "success": result,
            "message": "✅ Email đã gửi" if result else "❌ Email gửi thất bại"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("=" * 60)
    print("🚀 Flask API chạy trên:")
    print(f"  💻 PC:  http://localhost:5000")
    print(f"  📱 Điện thoại:  http://{local_ip}:5000")
    print("=" * 60)
    print("📡 Blockchain:", "✅ Kết nối thành công" if blockchain_service else "❌ Chưa kết nối")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
