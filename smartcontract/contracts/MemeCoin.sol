// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MemeCoin is ERC20 {
    // Constructor to initialize the token with a name, symbol, and initial supply
    constructor(string memory name, string memory symbol, uint256 initialSupply) ERC20(name, symbol) {
        // Mint the initial supply to the deployer of the contract
        // For meme coins, the supply can be very large, e.g., 1 trillion tokens
        _mint(msg.sender, initialSupply);
    }
}
