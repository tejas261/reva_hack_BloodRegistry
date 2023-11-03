// SPDX-Licence-Identifier: MIT
pragma solidity ^0.8.0;

contract BloodDonor{
    struct Donor{
        string d_name;
        string d_id;
        string d_email;
        string d_aadhar_no;
        string d_dob;
        string d_blood_type;
        uint256 blocked;
    }
    Donor[] public donors;
    mapping(string=>uint256) public index_to_donor;
    function badd(string memory d_name, string memory d_id, string memory d_email, string memory d_aadhar_no, string memory d_blood_type, string memory d_dob) public {
        donors.push(Donor({d_name:d_name,d_id:d_id,d_email:d_email,d_aadhar_no:d_aadhar_no,d_blood_type:d_blood_type,d_dob:d_dob,blocked:0}));
        uint256 l = donors.length-1;
        index_to_donor[d_id] = l;
    }
    function blogin(string memory d_id) public view returns(string memory, string memory, string memory, string memory, string memory){
        uint256 index = index_to_donor[d_id];
        Donor memory b = donors[index] ;
        return (b.d_name, b.d_email, b.d_aadhar_no, b.d_blood_type, b.d_dob) ;
    }
    function donor_view() public view returns(Donor[] memory){
        return donors;
    }
    function donor_details_from_aadhar(string memory d_id) public view returns(string memory,string memory){
        uint256 index = index_to_donor[d_id];
        Donor memory b = donors[index] ;
        return (b.d_name,b.d_blood_type);
    }
    function block_donor(string memory d_id) public view returns(Donor memory){
        uint256 index = index_to_donor[d_id];
        Donor memory b = donors[index] ;
        b.blocked = 1;
    }
    function check_blocked(string memory d_id) public view returns (uint256){
        uint256 index = index_to_donor[d_id];
        Donor memory b = donors[index] ;
        return b.blocked;
    }
}