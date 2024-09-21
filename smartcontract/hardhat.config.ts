import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from 'dotenv';
dotenv.config();

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.26",
    settings: {
      viaIR: true,
      evmVersion: "cancun",
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {
      hardfork: "cancun",
    },
    arbitrum: {
      url: "https://arb1.arbitrum.io/rpc", // Arbitrum One mainnet RPC URL
      accounts: [process.env.PRIVATE_KEY as string], // Replace with your wallet's private key
      gasPrice: 2000000000, // Optional: customize the gas price (in wei)
      
    },
  },
  etherscan: {
    // Use the Arbiscan API key for Arbitrum
    apiKey: {
      arbitrumOne: "H8TW72BIY8QK4JNAAIVRY4I53M1H49JWIA"
    },
  }
};

export default config;
