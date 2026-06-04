// SPDX-License-Identifier: CC BY 4.0
pragma solidity ^0.8.0;

/**
 * @title RiceDiseaseRecord
 * @dev Hệ thống blockchain lưu trữ thông tin bệnh lúa
 * Lưu trữ: Hình ảnh (IPFS hash), bệnh, thuốc, ngày phát hiện
 */

contract RiceDiseaseRecord {
    
    // Struct lưu trữ thông tin bệnh
    struct DiseaseRecord {
        uint256 id;
        address farmer;              // Địa chỉ nông dân
        string imageHash;            // IPFS hash của hình ảnh
        string[] diseases;           // Danh sách bệnh phát hiện
        string[] medications;        // Danh sách thuốc khuyến cáo
        string advice;               // Tư vấn từ AI
        uint256 timestamp;           // Thời gian ghi nhận
        string temperature;          // Điều kiện thời tiết (tùy chọn)
        string humidity;             // Độ ẩm (tùy chọn)
    }

    // Mapping lưu trữ tất cả các record
    mapping(uint256 => DiseaseRecord) public records;
    mapping(address => uint256[]) public farmerRecords;  // Record theo nông dân
    
    uint256 public recordCount = 0;
    
    // Events
    event DiseaseRecordCreated(
        uint256 indexed recordId,
        address indexed farmer,
        uint256 timestamp,
        string[] diseases
    );
    
    event DiseaseRecordUpdated(
        uint256 indexed recordId,
        address indexed farmer,
        uint256 timestamp
    );

    /**
     * @dev Tạo record bệnh mới
     * @param imageHash IPFS hash của hình ảnh
     * @param diseases Danh sách bệnh (tiếng Việt)
     * @param medications Danh sách thuốc điều trị
     * @param advice Tư vấn từ Groq AI
     * @param temperature Nhiệt độ môi trường
     * @param humidity Độ ẩm môi trường
     */
    function createRecord(
        string memory imageHash,
        string[] memory diseases,
        string[] memory medications,
        string memory advice,
        string memory temperature,
        string memory humidity
    ) public returns (uint256) {
        require(bytes(imageHash).length > 0, "Image hash cannot be empty");
        require(diseases.length > 0, "At least one disease must be recorded");
        require(medications.length > 0, "At least one medication must be recorded");

        uint256 newRecordId = recordCount;
        
        records[newRecordId] = DiseaseRecord(
            newRecordId,
            msg.sender,
            imageHash,
            diseases,
            medications,
            advice,
            block.timestamp,
            temperature,
            humidity
        );
        
        farmerRecords[msg.sender].push(newRecordId);
        recordCount++;
        
        emit DiseaseRecordCreated(newRecordId, msg.sender, block.timestamp, diseases);
        
        return newRecordId;
    }

    /**
     * @dev Lấy thông tin record theo ID
     */
    function getRecord(uint256 recordId) public view returns (DiseaseRecord memory) {
        require(recordId < recordCount, "Record does not exist");
        return records[recordId];
    }

    /**
     * @dev Lấy tất cả record của một nông dân
     */
    function getFarmerRecords(address farmer) public view returns (uint256[] memory) {
        return farmerRecords[farmer];
    }

    /**
     * @dev Lấy tổng số record
     */
    function getTotalRecords() public view returns (uint256) {
        return recordCount;
    }

    /**
     * @dev Lấy chi tiết các record của nông dân
     */
    function getFarmerRecordsDetails(address farmer) public view returns (DiseaseRecord[] memory) {
        uint256[] memory recordIds = farmerRecords[farmer];
        DiseaseRecord[] memory result = new DiseaseRecord[](recordIds.length);
        
        for (uint256 i = 0; i < recordIds.length; i++) {
            result[i] = records[recordIds[i]];
        }
        
        return result;
    }

    /**
     * @dev Cập nhật tư vấn của record (chỉ chủ sở hữu)
     */
    function updateAdvice(uint256 recordId, string memory newAdvice) public {
        require(recordId < recordCount, "Record does not exist");
        require(records[recordId].farmer == msg.sender, "Only record owner can update");
        
        records[recordId].advice = newAdvice;
        emit DiseaseRecordUpdated(recordId, msg.sender, block.timestamp);
    }
}
