// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const PoolmModule = buildModule("PoolmModule", (m) => {
  const contract = m.contract("PoolManager");

  return { contract };
});

export default PoolmModule;
