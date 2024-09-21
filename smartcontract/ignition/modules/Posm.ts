// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const PosmModule = buildModule("PosmModule", (m) => {
  const poolm = "0x40e0E511C5f7B7A3F111E6569aE6c07E6D6eBD2E";
  const allowTransfer = "0x5Af98aBf4f4AF98feB893c790334E533ef0d3246";

  const contract = m.contract("PositionManager", [poolm, allowTransfer, 10 ** 9]);

  return { contract };
});

export default PosmModule;
