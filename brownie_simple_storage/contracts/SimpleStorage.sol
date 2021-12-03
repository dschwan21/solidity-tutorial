// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;


contract SimpleStorage {
    
    uint256 favoriteNumber;
    
    struct People {
        uint favoriteNumber;
        string name;
    }
    
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;
    
  	function store(uint _favoriteNumber) public {
         favoriteNumber = _favoriteNumber;
    }
    
    // view, pure 
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
    
    function addPerson(string memory _name, uint256 _favoriteNumber) public{
        people.push(People( _favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}