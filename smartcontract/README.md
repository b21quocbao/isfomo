## Overview

- Utilizes Chainlink oracles to fetch emotion scores from an external API.
- Interacts with Uniswap V4 pools on the Arbitrum network.
- Enables users to collaboratively manage a liquidity pool based on the fetched emotion scores.
- Plans to implement more secure deposit and withdrawal methods, decentralizing liquidity management further.

## Prerequisites

Ensure you have the following installed:

- [Node.js](https://nodejs.org/) v14 or above
- [Hardhat](https://hardhat.org/getting-started/#installation)
- [MetaMask](https://metamask.io/) (for interacting with the deployed contract)

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-repo/IsFomo.git
   cd IsFomo
   ```

2. **Install dependencies:**

   ```bash
   cd smartcontract && npm install
   ```

3. **Create a `.env` file:**

   Create a `.env` file in the root directory with the following content:

   ```bash
   PRIVATE_KEY=YOUR_PRIVATE_KEY # to deploy
   ```

## Smart Contract Deployment

1. **Compile the contract:**

   ```bash
   npx hardhat compile
   ```

2. **Deploy the contract:**

   ```bash
   npx hardhat ignition deploy ./ignition/modules/IsFomo.ts --network arbitrum --verify
   ```

## Testing

   ```bash
   npx hardhat test
   ```

## Chainlink Oracle Setup

1. **Create a Chainlink Node:**

   Follow the [Chainlink node setup guide](https://docs.chain.link/docs/running-a-chainlink-node/) to create your own Chainlink node.

2. **Add an External Adapter:**

   Set up an external adapter to connect the Chainlink node to the API providing the emotion score.

3. **Create a Chainlink Job:**

   Use the following job specification to create a Chainlink job:

   ```json
   {
     "name": "Emotion Score Fetch",
     "initiators": [
       { "type": "runlog", "params": { "address": "YOUR_CONTRACT_ADDRESS" } }
     ],
     "tasks": [
       { "type": "httpGet", "params": { "get": "https://api.example.com/emotion" } },
       { "type": "jsonParse", "params": { "path": ["data", "score"] } },
       { "type": "multiply", "params": { "times": 100 } },
       { "type": "ethUint256" },
       { "type": "ethtx", "params": { "address": "YOUR_CONTRACT_ADDRESS" } }
     ]
   }
   ```

4. **Fund the Oracle Contract:**

   Fund the deployed contract with LINK tokens to cover the oracle service fees.

5. **Trigger Oracle Requests:**

   Use the contract’s function `requestEmotionScore()` to fetch the score from the oracle.

## Interacting with Deployed Contracts

1. **Connect to the Contract:**

   Use the following addresses to interact with the contracts on Arbitrum:

   - **TrumpCoin**: [0x0AB38A89CA6CC808cB255ECe2CCbf660d74ebeFe](https://arbiscan.io/token/0x0AB38A89CA6CC808cB255ECe2CCbf660d74ebeFe)
   - **USDC**: [0x643923795B6467Ebc877747ceb7eB6C8d1093EfF](https://arbiscan.io/token/0x643923795B6467Ebc877747ceb7eB6C8d1093EfF#code)
   - **IsFomo Contract**: [0xcCA6763EBf014f220484e8716938302A8419b7Ed](https://arbiscan.io/address/0xcCA6763EBf014f220484e8716938302A8419b7Ed#code)

## Future Work

**IsFomo** aims to enhance its smart contract functionality with the following features:

- **Secure Deposit and Withdrawal Mechanisms:**

  Implementing more secure and user-friendly methods for depositing and withdrawing tokens. This includes:

  - **Enhanced Security Measures:** Utilizing advanced security practices to protect user funds.
  - **User Authentication:** Incorporating mechanisms to verify user identities or permissions where appropriate.

- **Decentralized Liquidity Management:**

  Further decentralizing liquidity management by integrating directly with Uniswap pools or developing custom liquidity pools. This involves:

  - **Uniswap Pool Integration:**

    - Leveraging Uniswap V4's advanced features, such as hooks, to customize liquidity provision.
    - Allowing users to contribute to liquidity pools in a decentralized manner.

  - **Custom Pool Development:**

    - Creating bespoke liquidity pools tailored to the project's needs.
    - Implementing governance mechanisms for pool management.

- **Community Governance:**

  Introducing governance tokens or voting mechanisms to allow the community to have a say in protocol upgrades and parameter changes.

- **Improved User Interface:**

  Developing a user-friendly front-end application to interact with the IsFomo smart contract, making it accessible to non-technical users.

