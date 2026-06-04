"""
blockchain_service.py - Dịch vụ tích hợp Web3 cho hệ thống AI_Agri
Kết nối với Ganache và lưu dữ liệu lên blockchain
"""

import json
import os
from web3 import Web3
from datetime import datetime

class BlockchainService:
    def __init__(self, provider_url="http://127.0.0.1:8545", contract_address=None, contract_abi=None):
        """
        Khởi tạo dịch vụ blockchain
        
        Args:
            provider_url: URL của Ganache (mặc định: http://127.0.0.1:8545)
            contract_address: Địa chỉ smart contract đã deploy (nếu None sẽ dùng mặc định từ deployment)
            contract_abi: ABI của contract (hoặc load từ file)
        """
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        
        # Kiểm tra kết nối
        if not self.w3.is_connected():
            raise Exception("❌ Không thể kết nối đến Ganache. Hãy chắc chắn Ganache đang chạy!")
        
        print("✅ Kết nối Ganache thành công!")
        
        # Contract address từ deployment
        self.contract_address = contract_address or "0x5b1869D9A4C187F2EAa108f3062412ecf0526b24"
        self.contract = None
        self.abi = None
        
        # Tự động load ABI từ file build
        try:
            abi_path = os.path.join(os.path.dirname(__file__), "blockchain/build/contracts/RiceDiseaseRecord.json")
            if os.path.exists(abi_path):
                try:
                    with open(abi_path, 'r', encoding='utf-8-sig') as f:
                        contract_data = json.load(f)
                        self.abi = contract_data.get('abi')
                        print(f"✅ Loaded ABI từ {abi_path}")
                except UnicodeDecodeError:
                    with open(abi_path, 'r', encoding='latin-1') as f:
                        contract_data = json.load(f)
                        self.abi = contract_data.get('abi')
                        print(f"✅ Loaded ABI từ {abi_path} (with latin-1 encoding)")
            else:
                print(f"⚠️ Không tìm thấy ABI file: {abi_path}")
        except Exception as e:
            print(f"⚠️ Lỗi load ABI: {e}")
        
        if self.abi and self.contract_address:
            try:
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(self.contract_address),
                    abi=self.abi
                )
                print(f"✅ Contract initialized: {self.contract_address}")
            except Exception as e:
                print(f"⚠️ Lỗi khởi tạo contract: {e}")
        elif contract_abi:
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=contract_abi
            )

    def load_contract_abi(self, abi_file_path):
        """Load ABI từ file JSON (từ build/contracts/)"""
        try:
            # Thử load với encoding UTF-8 và xử lý BOM
            with open(abi_file_path, 'r', encoding='utf-8-sig') as f:
                contract_data = json.load(f)
                abi = contract_data.get('abi')
                if abi:
                    self.contract = self.w3.eth.contract(
                        address=Web3.to_checksum_address(self.contract_address),
                        abi=abi
                    )
                    self.abi = abi
                    print(f"✅ Loaded ABI từ {abi_file_path}")
                    return abi
        except UnicodeDecodeError:
            # Nếu UTF-8 fail, thử với encoding khác
            try:
                with open(abi_file_path, 'r', encoding='latin-1') as f:
                    contract_data = json.load(f)
                    abi = contract_data.get('abi')
                    if abi:
                        self.contract = self.w3.eth.contract(
                            address=Web3.to_checksum_address(self.contract_address),
                            abi=abi
                        )
                        self.abi = abi
                        print(f"✅ Loaded ABI từ {abi_file_path} (with latin-1 encoding)")
                        return abi
            except Exception as e:
                print(f"❌ Lỗi load ABI: {e}")
                return None
        except Exception as e:
            print(f"❌ Lỗi load ABI: {e}")
            return None

    def get_default_account(self):
        """Lấy tài khoản mặc định từ Ganache"""
        try:
            accounts = self.w3.eth.accounts
            if accounts:
                return accounts[0]
        except Exception as e:
            print(f"❌ Lỗi lấy account: {e}")
        return None

    def save_disease_record(self, image_hash, diseases, medications, advice, 
                           temperature="", humidity="", from_address=None):
        """
        Lưu record bệnh lúa lên blockchain
        
        Args:
            image_hash: IPFS hash hoặc hash của hình ảnh
            diseases: List tên bệnh (tiếng Việt)
            medications: List tên thuốc
            advice: Tư vấn từ AI
            temperature: Nhiệt độ (tùy chọn)
            humidity: Độ ẩm (tùy chọn)
            from_address: Địa chỉ nông dân (nếu None dùng default)
        
        Returns:
            Transaction hash nếu thành công, None nếu thất bại
        """
        if not self.contract:
            print("❌ Contract chưa được khởi tạo. Hãy load ABI trước!")
            return None
        
        if not from_address:
            from_address = self.get_default_account()
        
        try:
            # Chuẩn bị transaction
            tx_hash = self.contract.functions.createRecord(
                image_hash,
                diseases,
                medications,
                advice,
                temperature,
                humidity
            ).transact({'from': from_address})
            
            # Chờ transaction được xác nhận
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            print(f"✅ Record lưu thành công!")
            print(f"   TX Hash: {tx_hash.hex()}")
            print(f"   Block: {receipt['blockNumber']}")
            
            return {
                'tx_hash': tx_hash.hex(),
                'block_number': receipt['blockNumber'],
                'status': receipt['status'],
                'gas_used': receipt['gasUsed']
            }
        except Exception as e:
            print(f"❌ Lỗi lưu record: {e}")
            return None

    def get_record(self, record_id):
        """Lấy thông tin record từ blockchain"""
        if not self.contract:
            return None
        
        try:
            record = self.contract.functions.getRecord(record_id).call()
            return {
                'id': record[0],
                'farmer': record[1],
                'imageHash': record[2],
                'diseases': record[3],
                'medications': record[4],
                'advice': record[5],
                'timestamp': record[6],
                'temperature': record[7],
                'humidity': record[8]
            }
        except Exception as e:
            print(f"❌ Lỗi lấy record: {e}")
            return None

    def get_farmer_records(self, farmer_address):
        """Lấy tất cả record của nông dân"""
        if not self.contract:
            return None
        
        try:
            record_ids = self.contract.functions.getFarmerRecords(farmer_address).call()
            return record_ids
        except Exception as e:
            print(f"❌ Lỗi lấy farmer records: {e}")
            return None

    def get_farmer_records_details(self, farmer_address):
        """Lấy chi tiết tất cả record của nông dân"""
        if not self.contract:
            return None
        
        try:
            records = self.contract.functions.getFarmerRecordsDetails(farmer_address).call()
            result = []
            for record in records:
                result.append({
                    'id': record[0],
                    'farmer': record[1],
                    'imageHash': record[2],
                    'diseases': list(record[3]),
                    'medications': list(record[4]),
                    'advice': record[5],
                    'timestamp': record[6],
                    'temperature': record[7],
                    'humidity': record[8],
                    'date': datetime.fromtimestamp(record[6]).strftime("%d/%m/%Y %H:%M:%S")
                })
            return result
        except Exception as e:
            print(f"❌ Lỗi lấy chi tiết records: {e}")
            return None

    def get_total_records(self):
        """Lấy tổng số record trên blockchain"""
        if not self.contract:
            return 0
        
        try:
            total = self.contract.functions.getTotalRecords().call()
            return total
        except Exception as e:
            print(f"❌ Lỗi lấy total records: {e}")
            return 0

    def get_gas_price(self):
        """Lấy gas price hiện tại"""
        try:
            return self.w3.eth.gas_price
        except Exception as e:
            print(f"❌ Lỗi lấy gas price: {e}")
            return None

    def get_balance(self, address):
        """Lấy số dư ETH của address"""
        try:
            balance = self.w3.eth.get_balance(address)
            return self.w3.from_wei(balance, 'ether')
        except Exception as e:
            print(f"❌ Lỗi lấy balance: {e}")
            return None
