// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const MemeCoinModule = buildModule("MemeCoinModule", (m) => {
  const contract = m.contract("MemeCoin", ["DogeCoin", "DOGE", "1000000000000000000000000"]);

  return { contract };
});

export default MemeCoinModule;
