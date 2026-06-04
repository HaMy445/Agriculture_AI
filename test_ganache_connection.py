"""
test_blockchain_connection.py - Kiểm tra kết nối blockchain
Chạy script này để kiểm tra xem Ganache có đang chạy không
"""

from web3 import Web3

def test_ganache_connection():
    """Test kết nối đến Ganache"""
    print("=" * 60)
    print("🔗 TEST GANACHE CONNECTION")
    print("=" * 60)
    
    # Kết nối Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    
    if w3.is_connected():
        print("✅ KẾT NỐI THÀNH CÔNG!")
    else:
        print("❌ KẾT NỐI THẤT BẠI!")
        print("   Hãy chắc chắn Ganache đang chạy:")
        print("   ganache --host 127.0.0.1 --port 8545")
        return False
    
    # Lấy thông tin network
    print(f"\n📊 NETWORK INFO:")
    print(f"   Chain ID: {w3.eth.chain_id}")
    print(f"   Latest Block: {w3.eth.block_number}")
    print(f"   Gas Price: {w3.from_wei(w3.eth.gas_price, 'gwei')} Gwei")
    
    # Lấy accounts
    accounts = w3.eth.accounts
    print(f"\n👤 ACCOUNTS ({len(accounts)} total):")
    for i, account in enumerate(accounts[:5]):  # Hiển thị 5 accounts đầu
        balance = w3.eth.get_balance(account)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"   [{i}] {account} - {balance_eth} ETH")
    
    if len(accounts) > 5:
        print(f"   ... và {len(accounts) - 5} accounts khác")
    
    return True

if __name__ == "__main__":
    success = test_ganache_connection()
    print("\n" + "=" * 60)
    if success:
        print("✅ SẴN SÀNG DEPLOY SMART CONTRACT!")
        print("   Chạy: cd blockchain && truffle migrate --network development")
    else:
        print("❌ VUI LÒNG KHỞI ĐỘNG GANACHE TỪ")
    print("=" * 60)
