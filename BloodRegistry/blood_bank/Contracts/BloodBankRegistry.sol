// SPDX-Licence-Identifier: MIT
pragma solidity ^0.8.0;

contract BloodBank {
    struct Bank{
        string bb_name;
        string bb_id;
        string bb_email;
        string bb_licence_no;
        string bb_pwd;
        string bb_address;
        string bb_lat;
        string bb_long;
    }
    Bank[] public bank;
    // BloodDonor[] public DonorContractArray;
    // mapping(string=>address) public bbid_to_donors;
    mapping(string=>uint256) public index_to_bank;
    function add(string memory bb_name, string memory bb_id, string memory bb_email,
                 string memory bb_licence_no, string memory bb_pwd,
                 string memory bb_address,string memory bb_lat,string memory bb_long) public {
        bank.push(Bank({bb_name:bb_name,bb_id:bb_id,bb_email:bb_email,bb_licence_no:bb_licence_no,bb_pwd:bb_pwd,bb_address:bb_address,bb_lat:bb_lat,bb_long:bb_long}));
        uint256 l = bank.length-1;
        index_to_bank[bb_id] = l;
    }
    function login(string memory bb_id) public view
    returns(string memory, string memory, string memory, string memory, string memory, string memory ){
        uint256 index = index_to_bank[bb_id];
        Bank memory b = bank[index] ;
        return (b.bb_name, b.bb_email, b.bb_licence_no, b.bb_address, b.bb_lat, b.bb_long) ;
        
    }
    
    // function create_donor_contract_for_bank() public returns(address){
    //     BloodDonor bDonor = new BloodDonor();
    //     DonorContractArray.push(bDonor);
    //     return address(bDonor);
    // }
    // function get_address(string memory bb_id) public view returns(address){
    //     address b = bbid_to_donors[bb_id];
    //     return b;
    // }
}
