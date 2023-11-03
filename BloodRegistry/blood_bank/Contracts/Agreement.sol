// SPDX-Licence-Identifier: MIT
pragma solidity ^0.8.0;

contract Agreement{
    string hospital_id;
    string bloodBank_id;
    string bloodSample_id;
    string agreement_id;
    constructor(string memory h, string memory bb, string memory b, string memory a)  {
        hospital_id = h;
        bloodBank_id = bb;
        bloodSample_id = b;
        agreement_id = a;
    }
    function check_Hospital_query(string memory h_id) public view returns(bool){
        if (keccak256(abi.encodePacked(hospital_id)) == keccak256(abi.encodePacked(h_id))){
            return true;
        }
        return false;
    }
    function check_bloodBank_query(string memory bb_id) public view returns(bool){
        if (keccak256(abi.encodePacked(bb_id)) == keccak256(abi.encodePacked(bloodBank_id))){
            return true;
        }
        return false;
    }
    function check_bloodSample_query(string memory blood_id) public view returns(bool){
        if (keccak256(abi.encodePacked(blood_id)) == keccak256(abi.encodePacked(bloodSample_id))){
            return true;
        }
        return false;
    }
    function view_result() public view returns(string memory,string memory,string memory,string memory){
        return (hospital_id, bloodBank_id, bloodSample_id, agreement_id);
    }
}
