"""
blockchain_example.py - Ví dụ sử dụng BlockchainService
Chạy file này để test blockchain mà không cần Streamlit
"""

from blockchain_service import BlockchainService
import json

def main():
    print("=" * 60)
    print("🔗 BLOCKCHAIN SERVICE - RICE DISEASE EXAMPLE")
    print("=" * 60)
    
    # Khởi tạo blockchain service
    try:
        bs = BlockchainService(provider_url="http://127.0.0.1:8545")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        print("Hãy chắc chắn Ganache đang chạy: ganache --host 127.0.0.1 --port 8545")
        return
    
    # Lấy account mặc định
    account = bs.get_default_account()
    print(f"\n✅ Account: {account}")
    
    # Lấy balance
    balance = bs.get_balance(account)
    print(f"💰 Balance: {balance} ETH")
    
    # Load ABI từ file
    print("\n📄 Loading ABI...")
    abi = bs.load_contract_abi("blockchain/build/contracts/RiceDiseaseRecord.json")
    
    if not abi:
        print("❌ Không thể load ABI. Hãy chắc chắn đã compile & migrate contract")
        return
    
    # ⭐ THAY BẰNG CONTRACT ADDRESS CỦA BẠN (từ truffle migrate output)
    contract_address = "0x5b1869D9A4C187F2EAa108f3062412ecf0526b24"
    
    # Khởi tạo contract
    from web3 import Web3
    bs.contract = bs.w3.eth.contract(
        address=Web3.to_checksum_address(contract_address),
        abi=abi
    )
    print(f"✅ Contract loaded: {contract_address}")
    
    # Test 1: Tạo record bệnh
    print("\n" + "=" * 60)
    print("TEST 1: TẠO RECORD BỆNH MỚI")
    print("=" * 60)
    
    image_hash = "abc123def456ghi789jkl"
    diseases = ["Bệnh Đốm nâu", "Bệnh Bạc lá"]
    medications = ["Azoxystrobin", "Tebuconazole"]
    advice = "Phun thuốc trừ nấm mỗi 7-10 ngày. Đảm bảo ruộng thông thoáng."
    
    result = bs.save_disease_record(
        image_hash=image_hash,
        diseases=diseases,
        medications=medications,
        advice=advice,
        temperature="28°C",
        humidity="75%"
    )
    
    if result:
        print(f"\n✅ Lưu thành công!")
        print(f"   TX Hash: {result['tx_hash']}")
        print(f"   Block: {result['block_number']}")
        record_id = 0  # First record will have ID 0
    else:
        print("❌ Lưu thất bại")
        return
    
    # Test 2: Lấy record
    print("\n" + "=" * 60)
    print("TEST 2: LẤY THÔNG TIN RECORD")
    print("=" * 60)
    
    record = bs.get_record(record_id)
    if record:
        print(f"\n✅ Record ID: {record['id']}")
        print(f"   Farmer: {record['farmer']}")
        print(f"   Image Hash: {record['imageHash']}")
        print(f"   Diseases: {record['diseases']}")
        print(f"   Medications: {record['medications']}")
        print(f"   Timestamp: {record['timestamp']}")
    
    # Test 3: Lấy records của farmer
    print("\n" + "=" * 60)
    print("TEST 3: LẤY RECORDS CỦA FARMER")
    print("=" * 60)
    
    farmer_records = bs.get_farmer_records(account)
    print(f"\n✅ Farmer có {len(farmer_records)} records:")
    for rid in farmer_records:
        print(f"   - Record ID: {rid}")
    
    # Test 4: Lấy chi tiết records
    print("\n" + "=" * 60)
    print("TEST 4: LẤY CHI TIẾT RECORDS CỦA FARMER")
    print("=" * 60)
    
    records_detail = bs.get_farmer_records_details(account)
    if records_detail:
        print(f"\n✅ Chi tiết {len(records_detail)} records:")
        for i, rec in enumerate(records_detail):
            print(f"\n   Record {i+1}:")
            print(f"   - ID: {rec['id']}")
            print(f"   - Date: {rec['date']}")
            print(f"   - Diseases: {rec['diseases']}")
            print(f"   - Medications: {rec['medications']}")
    
    # Test 5: Tổng số records
    print("\n" + "=" * 60)
    print("TEST 5: TỔNG SỐ RECORDS TRÊN BLOCKCHAIN")
    print("=" * 60)
    
    total = bs.get_total_records()
    print(f"\n✅ Total records: {total}")
    
    # Test 6: Gas price
    print("\n" + "=" * 60)
    print("TEST 6: GAS PRICE")
    print("=" * 60)
    
    gas_price = bs.get_gas_price()
    print(f"\n✅ Gas Price: {bs.w3.from_wei(gas_price, 'gwei')} Gwei")
    
    print("\n" + "=" * 60)
    print("✅ TẤT CẢ TEST HOÀN THÀNH!")
    print("=" * 60)

if __name__ == "__main__":
    main()
