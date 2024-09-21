// This setup uses Hardhat Ignition to manage smart contract deployments.
// Learn more about it at https://hardhat.org/ignition

import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const IsFomoModule = buildModule("IsFomoModule", (m) => {
  const posmAddress = "0xF507901D3fc14b9a94c209F385A5C187f4C3F611";
  const poolmAddress = "0x40e0E511C5f7B7A3F111E6569aE6c07E6D6eBD2E";
  const allowTransferAddress = "0x5Af98aBf4f4AF98feB893c790334E533ef0d3246";

  const contract = m.contract("IsFomo", [posmAddress, poolmAddress, allowTransferAddress])

  return { contract };
});

export default IsFomoModule;
