import streamlit as st
from ultralytics import YOLO
from PIL import Image

import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import hashlib
import io
from blockchain_service import BlockchainService

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Rice AI - Local Server", layout="wide")

# Khởi tạo Groq

# --- KHỞI TẠO BLOCKCHAIN SERVICE ---
@st.cache_resource
def init_blockchain():
    try:
        bs = BlockchainService(provider_url="http://127.0.0.1:8545")
        return bs
    except Exception as e:
        st.warning(f"⚠️ Blockchain chưa sẵn sàng: {e}")
        return None

blockchain_service = init_blockchain()

# Tạo thư mục lưu trữ nếu chưa có
HISTORY_DIR = "history"
IMAGE_DIR = os.path.join(HISTORY_DIR, "images")
DATA_FILE = os.path.join(HISTORY_DIR, "data.json")

for path in [HISTORY_DIR, IMAGE_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)

# --- TỪ ĐIỂN TIẾNG VIỆT ---
vi_labels = {
    'Bacterial Leaf Blight': 'Bệnh Bạc lá (Vi khuẩn)',
    'Brown Spot': 'Bệnh Đốm nâu',
    'Healthy Leaf': 'Lá khỏe mạnh',
    'Leaf Blast Disease': 'Bệnh Đạo ôn (Cháy lá)',
    'Sheath Blight': 'Bệnh Khô vằn'
}

@st.cache_resource
def load_model():
    return YOLO("models/best.pt")

def get_treatment_advice(disease_name_vi):
    """Gọi Groq tư vấn"""
    prompt = f"Bạn là chuyên gia nông nghiệp VN. Hãy tư vấn điều trị bệnh '{disease_name_vi}' trên lúa ngắn gọn, có thuốc đặc trị. Nếu là lá khỏe mạnh thì trả lời 'Lá khỏe mạnh, không cần điều trị, chỉ đưa ra phương pháp chăm sóc tốt hơn'."
    try:
        chat_completion = client_groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except:
        return "⚠️ Không thể lấy tư vấn từ AI lúc này."

def send_gmail_notification(diseases, advice_text):
    # --- THÔNG TIN TÀI KHOẢN ---
    sender_email = "wuveil215@gmail.com"  
    receiver_email = "hamy5dvdsz@gmail.com"   # 📝 TODO: Cấu hình email nhận
    app_password = "kkeu aaum yikq zqlo" 

    # Kiểm tra email có hợp lệ không
    if not receiver_email or "@" not in receiver_email or receiver_email.startswith("("):
        print(f"⚠️ Email receiver không hợp lệ: {receiver_email}. Bỏ qua gửi email.")
        return False

    # --- NỘI DUNG EMAIL ---
    content = f"Hệ thống AI Agri DNU phát hiện: {', '.join(diseases)}\n\nTư vấn: {advice_text}"
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = "🚨 CẢNH BÁO BỆNH LÚA - DNU AI"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # --- THỰC HIỆN GỬI ---
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"ℹ️ Email không gửi được (có thể email chưa setup): {e}")
        return False

# --- HÀM LƯU TRỮ SERVER LOCAL VÀ BLOCKCHAIN (PHIÊN BẢN CŨ) ---
def save_to_local_server(image_pil, diseases, advice_text):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_filename = f"rice_{timestamp}.jpg"
        img_path = os.path.join(IMAGE_DIR, img_filename)
        
        image_pil.save(img_path)
        
        # ✅ HASH NỘI DUNG ẢNH (không phải đường dẫn)
        # Cách 1: Đọc byte từ file đã lưu
        with open(img_path, 'rb') as f:
            image_bytes = f.read()
        image_hash = hashlib.sha256(image_bytes).hexdigest()[:32]
        
        history_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        
        new_entry = {
            "id": timestamp,
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "diseases": diseases,
            "image_path": img_path,
            "image_hash": image_hash,
            "advice": advice_text,
            "blockchain_status": "pending"
        }
        history_data.insert(0, new_entry)
        
        # Lưu vào JSON local
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)
        
        # --- LƯU LÊN BLOCKCHAIN ---
        blockchain_result = None
        if blockchain_service:
            try:
                with st.spinner("⛓️ Đang lưu dữ liệu lên blockchain..."):
                    # Xử lý tư vấn: tách bệnh và thuốc từ advice_text
                    medications = []
                    lines = advice_text.split('\n')
                    for line in lines:
                        if any(med in line for med in ['Azoxystrobin', 'Tebuconazole', 'Pyraclostrobin', 
                                                        'Chlorothalonil', 'Mancozeb', 'Copper', 'Kasumin', 'Streptomycin']):
                            medications.append(line.strip())
                    
                    if not medications:
                        medications = ["Chưa có thông tin"]
                    
                    # Gọi blockchain để lưu record
                    blockchain_result = blockchain_service.save_disease_record(
                        image_hash=image_hash,
                        diseases=diseases,
                        medications=medications,
                        advice=advice_text[:500],  # Rút gọn advice để tiết kiệm gas
                        temperature="",
                        humidity=""
                    )
                    
                    if blockchain_result:
                        new_entry["blockchain_status"] = "confirmed"
                        new_entry["tx_hash"] = blockchain_result['tx_hash']
                        new_entry["block_number"] = blockchain_result['block_number']
                        
                        # Cập nhật JSON với thông tin blockchain
                        with open(DATA_FILE, "w", encoding="utf-8") as f:
                            json.dump(history_data, f, ensure_ascii=False, indent=4)
                        
                        st.success(f"✅ Dữ liệu lưu thành công trên blockchain!\nTX Hash: {blockchain_result['tx_hash'][:16]}...")
                    else:
                        st.warning("⚠️ Lưu blockchain thất bại, nhưng dữ liệu đã lưu local")
            except Exception as e:
                st.warning(f"⚠️ Lỗi blockchain: {e}\nDữ liệu đã lưu local")
        
        return True
    except Exception as e:
        st.error(f"Lỗi lưu trữ server: {e}")
        return False

# --- HÀM LƯU VỚI XÁC NHẬN VÀ TRACKING TỪNG BƯỚC ---
def handle_save_with_confirmation(image_pil, diseases, advice_text, uploaded_filename):
    """
    Luồng lưu dữ liệu với xác nhận và tracking từng bước
    Tương tự MetaMask popup + transaction tracking
    """
    
    # Step 0: CONFIRMATION DIALOG
    st.write("### 📋 Xác Nhận Lưu Dữ Liệu")
    
    confirm_col1, confirm_col2 = st.columns(2)
    with confirm_col1:
        st.info(f"""
        **Dữ liệu sẽ được lưu ở:**
        - 💾 Local Storage (JSON + Ảnh)
        - ⛓️ Blockchain (Smart Contract)
        - ✉️ Email Notification (nếu có)
        
        **Bệnh phát hiện:** {', '.join(diseases)}
        """)
    
    with confirm_col2:
        st.warning("""
        ⚠️ **Lưu ý:**
        - Không thể xóa dữ liệu từ blockchain
        - Lưu blockchain sẽ tốn Gas fee
        - Quá trình có thể mất 3-5 giây
        """)
    
    # Nút xác nhận
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        confirm_btn = st.button("✅ Xác Nhận", key=f"confirm_{uploaded_filename}")
    
    with col_btn2:
        cancel_btn = st.button("❌ Hủy", key=f"cancel_{uploaded_filename}")
    
    if cancel_btn:
        st.info("🚫 Đã hủy lưu dữ liệu")
        return False
    
    if not confirm_btn:
        return None  # Chờ user click
    
    # Step 1: LƯU LOCAL
    st.write("---")
    st.write("### 🔄 TIẾN TRÌNH LƯU DỮ LIỆU")
    
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    result_placeholder = st.empty()
    
    try:
        # Step 1: Save Local
        with status_placeholder.container():
            st.info("📝 **BƯỚC 1/3:** Đang lưu ảnh & metadata cục bộ...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_filename = f"rice_{timestamp}.jpg"
        img_path = os.path.join(IMAGE_DIR, img_filename)
        
        image_pil.save(img_path)
        
        # Hash ảnh
        with open(img_path, 'rb') as f:
            image_bytes = f.read()
        image_hash = hashlib.sha256(image_bytes).hexdigest()[:32]
        
        # Load history data
        history_data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                history_data = json.load(f)
        
        new_entry = {
            "id": timestamp,
            "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "diseases": diseases,
            "image_path": img_path,
            "image_hash": image_hash,
            "advice": advice_text,
            "blockchain_status": "pending"
        }
        history_data.insert(0, new_entry)
        
        # Save to JSON
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, ensure_ascii=False, indent=4)
        
        with status_placeholder.container():
            st.success("✅ **BƯỚC 1/3 HOÀN TẤT:** Ảnh & metadata lưu thành công")
            st.markdown(f"- 📁 Ảnh: `{img_filename}`")
            st.markdown(f"- 🔐 Hash: `{image_hash}`")
        
        # Step 2: Save Blockchain
        with status_placeholder.container():
            st.info("📝 **BƯỚC 1/3 HOÀN TẤT:** ✅\n⛓️ **BƯỚC 2/3:** Đang lưu dữ liệu lên blockchain...")
        
        blockchain_result = None
        if blockchain_service:
            # Xử lý medications
            medications = []
            lines = advice_text.split('\n')
            for line in lines:
                if any(med in line for med in ['Azoxystrobin', 'Tebuconazole', 'Pyraclostrobin', 
                                                'Chlorothalonil', 'Mancozeb', 'Copper', 'Kasumin', 'Streptomycin']):
                    medications.append(line.strip())
            
            if not medications:
                medications = ["Chưa có thông tin"]
            
            # Call blockchain service
            blockchain_result = blockchain_service.save_disease_record(
                image_hash=image_hash,
                diseases=diseases,
                medications=medications,
                advice=advice_text[:500],
                temperature="",
                humidity=""
            )
            
            if blockchain_result:
                new_entry["blockchain_status"] = "confirmed"
                new_entry["tx_hash"] = blockchain_result['tx_hash']
                new_entry["block_number"] = blockchain_result['block_number']
                
                # Update JSON
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(history_data, f, ensure_ascii=False, indent=4)
                
                with status_placeholder.container():
                    st.success("✅ **BƯỚC 2/3 HOÀN TẤT:** Lưu blockchain thành công")
                    st.markdown(f"- 🔗 Transaction Hash: `{blockchain_result['tx_hash'][:20]}...`")
                    st.markdown(f"- 📦 Block Number: `{blockchain_result['block_number']}`")
                
                # Step 3: Final result
                with status_placeholder.container():
                    st.info("📝 **BƯỚC 1/3 HOÀN TẤT:** ✅\n⛓️ **BƯỚC 2/3 HOÀN TẤT:** ✅\n✅ **BƯỚC 3/3:** Hoàn tất")
                
                # Show final success
                with result_placeholder.container():
                    st.write("---")
                    st.success("🎉 **TẤT CẢ BƯỚC HOÀN TẤT THÀNH CÔNG!**")
                    
                    result_col1, result_col2 = st.columns(2)
                    
                    with result_col1:
                        st.markdown("""
                        ### 💾 LOCAL STORAGE
                        - ✅ Ảnh lưu thành công
                        - ✅ Metadata lưu vào data.json
                        - ✅ Có thể truy cập lại lịch sử
                        """)
                    
                    with result_col2:
                        st.markdown(f"""
                        ### ⛓️ BLOCKCHAIN RECORD
                        - ✅ Đã ghi lên smart contract
                        - **TX Hash:** `{blockchain_result['tx_hash'][:16]}...`
                        - **Block:** `{blockchain_result['block_number']}`
                        - ✅ Vĩnh viễn & bất biến
                        """)
                
                return True
            else:
                st.warning("⚠️ Lưu blockchain thất bại, nhưng dữ liệu đã lưu local")
                return True
        else:
            st.warning("⚠️ Blockchain không sẵn sàng, dữ liệu đã lưu local")
            return True
    
    except Exception as e:
        with result_placeholder.container():
            st.error(f"❌ Lỗi trong quá trình lưu: {str(e)}")
        return False

# --- GIAO DIỆN CHÍNH ---
st.sidebar.title("Nhận diện sâu bệnh lúa - DNU")
page = st.sidebar.radio("Chọn chức năng", [
    "Nhận diện bệnh", 
    "Lịch sử hệ thống",
    "Blockchain Records"
])

if page == "Nhận diện bệnh":
    st.title("🌾 Chẩn đoán & Lưu trữ Local")
    uploaded_file = st.file_uploader("Tải ảnh lá lúa...", type=["jpg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Ảnh gốc", width='stretch')
            
        with st.spinner("AI đang xử lý..."):
            model = load_model()
            results = model.predict(image)
            
        with col2:
            if len(results[0].boxes) > 0:
                for i, eng_name in results[0].names.items():
                    if eng_name in vi_labels:
                        results[0].names[i] = vi_labels[eng_name]
                
                res_plotted = results[0].plot()
                st.image(res_plotted, caption="Kết quả nhận diện", width='stretch')
                unique_diseases = list(set([results[0].names[int(box.cls[0])] for box in results[0].boxes]))
            else:
                st.success("Lá lúa khỏe mạnh!")
                unique_diseases = []

        if unique_diseases:
            st.write("---")
            advice_content = ""
            for d in unique_diseases:
                with st.expander(f"Điều trị {d}", expanded=True):
                    res = get_treatment_advice(d)
                    st.markdown(res)
                    advice_content += f"{d}: {res}\n"
            
            # --- TỰ ĐỘNG GỬI EMAIL KHI PHÁT HIỆN BỆNH ---
            # Kiểm tra xem file này đã được gửi email tự động chưa để tránh gửi lặp
            state_key = f"sent_{uploaded_file.name}"
            if state_key not in st.session_state:
                with st.spinner("🚨 Phát hiện bệnh! Đang tự động gửi báo cáo Gmail..."):
                    if send_gmail_notification(unique_diseases, advice_content):
                        st.toast("📱 Báo cáo tự động đã được gửi tới Gmail!", icon="📧")
                        st.session_state[state_key] = True # Đánh dấu đã gửi thành công
                    else:
                        st.warning("Tự động gửi Gmail thất bại. Vui lòng kiểm tra kết nối.")

            # --- NÚT LƯU VỚI XÁC NHẬN VÀ TRACKING ---
            if st.button("💾 Lưu kết quả vào Lịch sử", key=f"save_btn_{uploaded_file.name}"):
                st.session_state[f"save_confirm_{uploaded_file.name}"] = True
            
            # Hiển thị dialog xác nhận nếu user click button
            if st.session_state.get(f"save_confirm_{uploaded_file.name}", False):
                handle_save_with_confirmation(image, unique_diseases, advice_content, uploaded_file.name)
                st.session_state[f"save_confirm_{uploaded_file.name}"] = False

elif page == "Lịch sử hệ thống":
    st.title("📜 Danh sách ca bệnh đã lưu")
    
    if blockchain_service:
        col1, col2, col3 = st.columns(3)
        with col1:
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        local_data = json.load(f)
                        local_count = len(local_data)
                except:
                    local_count = 0
            else:
                local_count = 0
            st.metric("💾 Total Records Local", local_count)
        with col2:
            total_blockchain = blockchain_service.get_total_records()
            st.metric("⛓️ Total Records Blockchain", total_blockchain)
        with col3:
            default_account = blockchain_service.get_default_account()
            if default_account:
                balance = blockchain_service.get_balance(default_account)
                st.metric("💰 Account Balance (ETH)", f"{balance:.4f}" if balance else "Error")
    
    st.write("---")
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        for item in data:
            with st.container(border=True):
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.image(item["image_path"], width='stretch')
                with c2:
                    st.write(f"**Thời gian:** {item['time']}")
                    st.write(f"**Bệnh:** {', '.join(item['diseases'])}")
                    st.info(item["advice"][:300] + "...")
                    
                    # Hiển thị thông tin blockchain nếu có
                    if item.get("blockchain_status"):
                        if item["blockchain_status"] == "confirmed":
                            st.success(f"✅ Blockchain: {item.get('tx_hash', 'N/A')[:16]}... (Block: {item.get('block_number', 'N/A')})")
                        else:
                            st.warning(f"⏳ Blockchain: {item['blockchain_status']}")
    else:
        st.write("Chưa có lịch sử lưu trữ nào.")

elif page == "Blockchain Records":
    st.title("⛓️ Blockchain Records - Tất cả ca bệnh trên blockchain")
    
    if not blockchain_service:
        st.error("❌ Blockchain chưa sẵn sàng. Hãy chắc chắn Ganache đang chạy!")
    else:
        # --- THỐNG KÊ BLOCKCHAIN ---
        st.write("### 📊 Thống kê Blockchain")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_records = blockchain_service.get_total_records()
            st.metric("📝 Total Records", total_records)
        
        with col2:
            default_account = blockchain_service.get_default_account()
            if default_account:
                balance = blockchain_service.get_balance(default_account)
                st.metric("💰 Account Balance", f"{balance:.4f} ETH" if balance else "Error")
        
        with col3:
            gas_price = blockchain_service.get_gas_price()
            if gas_price:
                gas_gwei = blockchain_service.w3.from_wei(gas_price, 'gwei')
                st.metric("⚡ Gas Price", f"{gas_gwei:.0f} Gwei")
        
        st.write("---")
        
        # --- DANH SÁCH RECORDS TỪ BLOCKCHAIN ---
        if default_account:
            st.write("### 📋 Chi tiết Records trên Blockchain")
            
            blockchain_records = blockchain_service.get_farmer_records_details(default_account)
            
            if blockchain_records and len(blockchain_records) > 0:
                # Hiển thị từ mới nhất tới cũ nhất
                for i, record in enumerate(reversed(blockchain_records)):
                    with st.container(border=True):
                        col_left, col_right = st.columns([2, 1])
                        
                        with col_left:
                            st.markdown(f"**• Bệnh:** {', '.join(record['diseases'])}")
                            st.markdown(f"**📋 Thời gian:** {record['date']}")
                            st.markdown(f"**👨‍🌾 Nông dân:** `{record['farmer'][:18]}...`")
                            
                            # Tư vấn
                            if record['advice']:
                                advice_short = record['advice'][:100]
                                if len(record['advice']) > 100:
                                    advice_short += "..."
                                st.markdown(f"**💊 Tư vấn:** {advice_short}")
                                
                                # Thuốc khuyến cáo
                                if record['medications'] and record['medications'][0] != "Chưa có thông tin":
                                    st.markdown(f"**🔬 Thuốc:** {', '.join(record['medications'][:3])}")
                        
                        with col_right:
                            st.markdown(f"**ID:** {record['id']}")
                            st.markdown(f"**Hash:** `{record['imageHash'][:12]}...`")
                            st.markdown(f"**Block:** `{record['timestamp']}`")
                            
                            # TX Info (nếu có)
                            if os.path.exists(DATA_FILE):
                                try:
                                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                                        local_data = json.load(f)
                                        # Tìm matching record
                                        for item in local_data:
                                            if str(record['id']) in str(item.get('id', '')):
                                                if item.get('tx_hash'):
                                                    st.markdown(f"**TX:** `{item['tx_hash'][:10]}...`")
                                                    break
                                except:
                                    pass
            else:
                st.info("📭 Chưa có records nào trên blockchain")
        else:
            st.error("❌ Không thể lấy account từ Ganache")