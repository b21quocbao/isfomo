// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract USDCToken is ERC20, Ownable {
    // Constructor to initialize the token with a name, symbol, and initial supply
    constructor(
        uint256 initialSupply
    ) ERC20("USD Coin", "USDC") Ownable(msg.sender) {
        // Mint the initial supply to the deployer of the contract with 6 decimals
        _mint(msg.sender, initialSupply * (10 ** uint256(decimals())));
    }

    // Override the decimals function to return 6, which is the standard for USDC
    function decimals() public view virtual override returns (uint8) {
        return 6;
    }

    // Mint new tokens (only the owner can call this function)
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    // Burn tokens (only the owner can call this function)
    function burn(address from, uint256 amount) external onlyOwner {
        _burn(from, amount);
    }
}
