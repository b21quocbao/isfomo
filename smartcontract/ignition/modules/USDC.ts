// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const USDCModule = buildModule("USDCModule", (m) => {
  const contract = m.contract("USDCToken", ["1000000000000"]);

  return { contract };
});

export default USDCModule;
