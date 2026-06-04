# 🏗️ ARCHITECTURE - AI_AGRI WITH BLOCKCHAIN

## 📐 SYSTEM ARCHITECTURE DIAGRAM

```
┌──────────────────────────────────────────────────────────────────┐
│                     STREAMLIT WEB INTERFACE                      │
│                      (http://localhost:8501)                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │                    2 MAIN PAGES                            │  │
│  ├────────────────────────────────────────────────────────────┤  │
│  │ 1. "Nhận diện bệnh"                                        │  │
│  │    - Upload ảnh lá lúa (JPG/PNG)                          │  │
│  │    - Hiển thị ảnh phát hiện bệnh                          │  │
│  │    - Tư vấn điều trị từ AI                                │  │
│  │    - Nút "Lưu kết quả"                                     │  │
│  │                                                            │  │
│  │ 2. "Lịch sử hệ thống"                                      │  │
│  │    - Danh sách tất cả ca bệnh                             │  │
│  │    - Ảnh bệnh + thuốc đề nghị                             │  │
│  │    - TX Hash & Block Number (blockchain)                  │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
    ↓                    ↓                    ↓
┌───────────────┐ ┌─────────────────┐ ┌──────────────────┐
│  YOLOv8 AI    │ │   Groq LLM AI   │ │  Email Sender    │
│ (models/      │ │  (Treatment     │ │  (Gmail SMTP)    │
│  best.pt)     │ │   Advice)       │ │                  │
│               │ │                 │ │ Receiver:        │
│ Detects:      │ │ Model:          │ │ hamy572002@...   │
│ • Bacterial   │ │ llama-3.3-70b   │ │                  │
│   Leaf Blight │ │                 │ │ Auto-send when   │
│ • Brown Spot  │ │ Output:         │ │ disease detected │
│ • Healthy Leaf│ │ Drug treatment  │ │                  │
│ • Leaf Blast  │ │ recommendations │ │ Status: ✅ Ready │
│ • Sheath      │ │                 │ │                  │
│   Blight      │ │ Status: ✅      │ │                  │
│               │ │ API Key: ✅     │ │                  │
│ Status: ✅    │ │                 │ │                  │
│ Model: ✅     │ └─────────────────┘ └──────────────────┘
└───────────────┘
    ↓
┌────────────────────────────────────────────────────────────┐
│         PYTHON APPLICATION (app.py)                        │
├────────────────────────────────────────────────────────────┤
│ • Process user input                                       │
│ • Integrate AI models                                      │
│ • Format data for storage                                  │
└────────────────────────────────────────────────────────────┘
    ↓                                    ↓
┌──────────────────────────┐  ┌─────────────────────────────┐
│   LOCAL STORAGE          │  │  BLOCKCHAIN STORAGE         │
│   (File System)          │  │  (Smart Contract)           │
├──────────────────────────┤  ├─────────────────────────────┤
│ history/                 │  │ RiceDiseaseRecord.sol       │
│ ├─ data.json             │  │                             │
│ │ {                      │  │ Network: Ganache            │
│ │   id,                  │  │ Address: 127.0.0.1:8545     │
│ │   time,                │  │ Chain ID: 1337              │
│ │   diseases,            │  │                             │
│ │   image_path,          │  │ Functions:                  │
│ │   image_hash,          │  │ • createRecord()            │
│ │   advice,              │  │ • getRecord()               │
│ │   tx_hash ⭐,          │  │ • getFarmerRecords()        │
│ │   block_number ⭐      │  │ • updateAdvice()            │
│ │ }                      │  │                             │
│ │                        │  │ Events:                     │
│ └─ images/               │  │ • DiseaseRecordCreated      │
│    ├─ rice_*.jpg         │  │ • DiseaseRecordUpdated      │
│    └─ (all images)       │  │                             │
│                          │  │ Status: ✅ Ready            │
│ Status: ✅ Ready         │  │ Solidity: ^0.8.0            │
└──────────────────────────┘  └─────────────────────────────┘
         ↓                              ↓
    ┌─────────────────────────────────────────┐
    │  BLOCKCHAIN SERVICE (blockchain_service.py)
    ├─────────────────────────────────────────┤
    │ Python Module: Web3 Integration         │
    │                                         │
    │ Functions:                              │
    │ • init_blockchain()                     │
    │ • load_contract_abi()                   │
    │ • save_disease_record()    ⭐ Main      │
    │ • get_record()                          │
    │ • get_farmer_records()                  │
    │ • get_total_records()                   │
    │ • get_balance()                         │
    │                                         │
    │ Status: ✅ Ready                        │
    └─────────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────────┐
    │  GANACHE (Local Ethereum)               │
    ├─────────────────────────────────────────┤
    │ • Localhost: 127.0.0.1:8545             │
    │ • 10 Pre-funded Accounts (100 ETH each) │
    │ • Instant Transaction Confirmation      │
    │                                         │
    │ Features:                               │
    │ • Deterministic (seed-based)            │
    │ • Gas simulation                        │
    │ • Web3 compatible                       │
    │                                         │
    │ Status: ✅ Ready to install             │
    │ Command: ganache --host 127.0.0.1 --   │
    │          port 8545 --deterministic     │
    └─────────────────────────────────────────┘
```

---

## 🔄 DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ACTION                              │
│              Upload Image + Detect Disease                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│               YOLOV8 INFERENCE ENGINE                        │
│         Load Model → Process Image → Detect Disease         │
│                                                              │
│ Input: Image (JPG/PNG)                                      │
│ Output: Bounding boxes, class predictions, confidence       │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              DISEASE CLASSIFICATION                          │
│          Translate to Vietnamese + Format Results           │
│                                                              │
│ vi_labels = {                                               │
│   'Bacterial Leaf Blight': 'Bệnh Bạc lá (Vi khuẨn)',       │
│   'Brown Spot': 'Bệnh Đốm nâu',                             │
│   ...                                                        │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              GROQ LLM AI CONSULTATION                        │
│         Get Treatment Advice for Each Disease               │
│                                                              │
│ Prompt: "Tư vấn điều trị bệnh [name] trên lúa..."          │
│ Response: Specific drugs (Azoxystrobin, etc.)               │
└─────────────────────────────────────────────────────────────┘
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
        ┌──────────────┐      ┌─────────────────────┐
        │ AUTO EMAIL   │      │ USER ACTION:        │
        │ NOTIFICATION │      │ Click "Lưu kết quả" │
        ├──────────────┤      └─────────────────────┘
        │ • Disease    │              ↓
        │ • Treatment  │      ┌─────────────────────┐
        │ • Advice     │      │ SAVE DATA LOCALLY   │
        │              │      ├─────────────────────┤
        │ To:          │      │ • Save JPG image    │
        │ hamy572002   │      │ • Create hash       │
        │ @gmail.com   │      │ • Append JSON       │
        │              │      │ • metadata          │
        │ Auto-sent ✅ │      │                     │
        └──────────────┘      └─────────────────────┘
                                     ↓
                         ┌─────────────────────────┐
                         │ BLOCKCHAIN SERVICE      │
                         │ (blockchain_service.py) │
                         └─────────────────────────┘
                                     ↓
                    ┌────────────────┴────────────────┐
                    ↓                                 ↓
        ┌─────────────────────┐        ┌──────────────────────┐
        │  WEB3.PY CONNECTION │        │  SMART CONTRACT CALL │
        ├─────────────────────┤        ├──────────────────────┤
        │ Connect to:         │        │ Function:            │
        │ http://127.0.0.1:   │        │ createRecord(        │
        │ 8545 (Ganache)      │        │   imageHash,         │
        │                     │        │   diseases[],        │
        │ Check connection ✅ │        │   medications[],     │
        │                     │        │   advice,            │
        │ Get account address │        │   temp, humidity     │
        │ (default: 1st in    │        │ )                    │
        │ Ganache list)       │        │                      │
        └─────────────────────┘        │ Return: Record ID    │
                    ↓                  └──────────────────────┘
                    └─────────────────────┬──────────────────────┘
                                          ↓
                    ┌─────────────────────────────────────┐
                    │   GANACHE BLOCKCHAIN                │
                    ├─────────────────────────────────────┤
                    │ • Create Transaction                │
                    │ • Add to memory pool                │
                    │ • Mine Block                        │
                    │ • Execute contract function         │
                    │ • Update state (storage)            │
                    │ • Return Receipt with:              │
                    │   - Transaction Hash ⭐             │
                    │   - Block Number ⭐                 │
                    │   - Gas Used ⭐                     │
                    │   - Status: 1 (success)             │
                    └─────────────────────────────────────┘
                                          ↓
                    ┌─────────────────────────────────────┐
                    │  UPDATE LOCAL JSON WITH BLOCKCHAIN  │
                    │  INFO (tx_hash, block_number, etc)  │
                    └─────────────────────────────────────┘
                                          ↓
                    ┌─────────────────────────────────────┐
                    │  DISPLAY SUCCESS MESSAGE            │
                    │  Show TX Hash in Streamlit          │
                    │  ✅ Record saved on blockchain!     │
                    └─────────────────────────────────────┘
                                          ↓
                    ┌─────────────────────────────────────┐
                    │  HISTORY PAGE DISPLAY               │
                    │ • Show all previous records         │
                    │ • Display TX hash & block no.       │
                    │ • Verify on blockchain              │
                    └─────────────────────────────────────┘
```

---

## 🏢 DEPLOYMENT ARCHITECTURE

```
LOCAL MACHINE (Development)
│
├── PORT 8501 (Streamlit)
│   └── Web UI for users
│
├── PORT 8545 (Ganache RPC)
│   └── Local Ethereum blockchain
│       ├── Account 0: Nông dân 1 (100 ETH)
│       ├── Account 1: Nông dân 2 (100 ETH)
│       └── ... 8 more accounts
│
├── PROCESSES
│   ├── Streamlit App (Python)
│   ├── Ganache (Node.js)
│   └── Web3.py Bridge (Python)
│
└── STORAGE
    ├── history/data.json (Local metadata)
    ├── history/images/* (Rice images)
    └── blockchain/build/ (Smart contract ABI)

BLOCKCHAIN STATE (In Ganache Memory)
│
├── RiceDiseaseRecord Contract
│   ├── Mapping: records[id] → DiseaseRecord
│   ├── Mapping: farmerRecords[address] → id[]
│   └── Counter: recordCount (0, 1, 2, ...)
│
└── Each Record Contains:
    ├── id (uint256)
    ├── farmer (address)
    ├── imageHash (string)
    ├── diseases[] (array of strings)
    ├── medications[] (array of strings)
    ├── advice (string)
    ├── timestamp (uint256)
    ├── temperature (string)
    └── humidity (string)
```

---

## 🔌 COMPONENT INTEGRATION

```
┌──────────────────────────────────────────────────────────────┐
│                   Streamlit Frontend                         │
│                    (Presentation Layer)                      │
└──────────────────────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────────────────────┐
│                 Application Logic Layer                       │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│  │  YOLO Model    │  │  Groq LLM      │  │  Email Sender  │ │
│  │  (Detection)   │  │  (Advice)      │  │  (Notification)│ │
│  └────────────────┘  └────────────────┘  └────────────────┘ │
└──────────────────────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────────────────────┐
│              Data Persistence Layer                           │
│  ┌────────────────┐               ┌───────────────────────┐ │
│  │   Local File   │               │  Blockchain Service   │ │
│  │   System       │               │  (Web3 Module)        │ │
│  │  (JSON + JPG)  │               │                       │ │
│  └────────────────┘               └───────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────────────────────┐
│              Blockchain Layer                                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│  │  Smart         │  │  Web3.py       │  │  Ganache       │ │
│  │  Contract      │  │  Connection    │  │  Blockchain    │ │
│  │  (Solidity)    │  │  (Python)      │  │  (Local)       │ │
│  └────────────────┘  └────────────────┘  └────────────────┘ │
└──────────────────────────────────────────────────────────────┘
              ↓
┌──────────────────────────────────────────────────────────────┐
│              Blockchain State                                 │
│  ├─ RiceDiseaseRecord mappings                               │
│  ├─ DiseaseRecord structs                                    │
│  ├─ Transaction receipts                                     │
│  └─ Block history                                            │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 DATABASE SCHEMA (Blockchain)

```sql
-- Smart Contract Storage (Ganache)

TABLE: records (mapping uint256 => DiseaseRecord)
┌─────────┬──────────┬──────────┬────────┬──────────┬────────┬───────────┬────────────┬─────────┐
│ id      │ farmer   │ imgHash  │ diseases │ med.    │ advice │ timestamp │ temp.      │ humidity│
├─────────┼──────────┼──────────┼────────┼──────────┼────────┼───────────┼────────────┼─────────┤
│ uint256 │ address  │ string   │ string[] │ string[] │ string │ uint256  │ string     │ string │
├─────────┼──────────┼──────────┼────────┼──────────┼────────┼───────────┼────────────┼─────────┤
│ 0       │ 0x1234...│ abc123..│ [       │ [        │ Phun...│ 1715002..|28°C       │ 75%    │
│         │          │         │ "Bệnh"  │"Azoxy"   │        │          │            │        │
├─────────┼──────────┼──────────┼────────┼──────────┼────────┼───────────┼────────────┼─────────┤
│ 1       │ 0x1234...│ def456..│ [       │ [        │ Tư vấn.│ 1715003..|29°C       │ 72%    │
│         │          │         │ "Bệnh2" │"Tebu"    │        │          │            │        │
└─────────┴──────────┴──────────┴────────┴──────────┴────────┴───────────┴────────────┴─────────┘

TABLE: farmerRecords (mapping address => uint256[])
┌──────────────────────────────┬─────────────────────┐
│ farmer (address)             │ record_ids (uint[]) │
├──────────────────────────────┼─────────────────────┤
│ 0x1234567890...              │ [0, 1, 3, 5]        │
├──────────────────────────────┼─────────────────────┤
│ 0xabcdef0123...              │ [2, 4]              │
└──────────────────────────────┴─────────────────────┘

TABLE: recordCount (global counter)
┌─────────────┐
│ count       │
├─────────────┤
│ 6           │ (Next record will be ID 6)
└─────────────┘
```

---

## 🔐 SECURITY CONSIDERATIONS

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY MODEL                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 1. AUTHENTICATION                                            │
│    ├─ Ganache default accounts (pre-funded)                │
│    ├─ No private key needed (local dev)                    │
│    └─ Production: Use MetaMask/WalletConnect               │
│                                                              │
│ 2. AUTHORIZATION                                            │
│    ├─ Only farmer can update their own records             │
│    ├─ Smart contract enforces via msg.sender check         │
│    └─ Immutable record creation (no deletion)              │
│                                                              │
│ 3. DATA INTEGRITY                                           │
│    ├─ Image hash prevents tampering                        │
│    ├─ Block hash ensures blockchain integrity              │
│    └─ Timestamp prevents time manipulation                 │
│                                                              │
│ 4. PRIVACY                                                   │
│    ├─ Ganache runs locally (no external exposure)          │
│    ├─ All data on-chain is transparent (by design)         │
│    └─ Production: Consider privacy layers                  │
│                                                              │
│ 5. COMPLIANCE                                                │
│    ├─ CC BY 4.0 License                                    │
│    ├─ Data ownership: Each farmer owns their records       │
│    └─ Audit trail: All transactions permanent              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 SCALABILITY ROADMAP

```
PHASE 1: Local Development (Current)
├─ Ganache blockchain
├─ Single machine deployment
├─ ~100 records per session
└─ Perfect for testing ✅

PHASE 2: Testnet Deployment
├─ Deploy to Sepolia/Mumbai testnet
├─ Real Ethereum testnet experience
├─ Unlimited records (free test ETH)
└─ Public verification possible

PHASE 3: Mainnet Production
├─ Deploy to Ethereum/Polygon mainnet
├─ Real economic incentives
├─ IPFS integration for images
├─ The Graph indexing
└─ 1000+ farmers support

PHASE 4: Optimization
├─ Layer 2 solutions (Arbitrum, Optimism)
├─ Sidechain aggregation
├─ Off-chain data with on-chain verification
└─ Enterprise deployment
```

---

## ✅ CHECKLIST

- [x] Smart Contract created (Solidity)
- [x] Truffle configuration complete
- [x] Migration scripts ready
- [x] Web3 Python integration
- [x] Streamlit app updated
- [x] Local storage integrated
- [x] Email notifications working
- [x] Testing tools created
- [x] Documentation complete
- [x] All files organized

**Architecture: READY FOR DEPLOYMENT! 🚀**
