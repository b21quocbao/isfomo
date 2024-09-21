import {
  time,
  loadFixture,
} from "@nomicfoundation/hardhat-toolbox/network-helpers";
import { anyValue } from "@nomicfoundation/hardhat-chai-matchers/withArgs";
import { expect } from "chai";
import hre from "hardhat";
import { PoolKeyStruct } from "../typechain-types/contracts/IsFomo";

describe("IsFomoPoolManager", function () {
  const addDecimal = (n: number, k: number) => (BigInt(n) * BigInt(10 ** k)).toString();

  // We define a fixture to reuse the same setup in every test.
  // We use loadFixture to run this setup once, snapshot that state,
  // and reset Hardhat Network to that snapshot in every test.
  async function deployContracts() {
    // Contracts are deployed using the first signer/account by default
    const [owner, user1, user2] = await hre.ethers.getSigners();

    const PoolManager = await hre.ethers.getContractFactory("PoolManager");
    const PositionManager = await hre.ethers.getContractFactory("PositionManager");
    const IsFomo = await hre.ethers.getContractFactory("IsFomo");
    const AllowanceTransfer = await hre.ethers.getContractFactory("AllowanceTransfer");
    const USDCToken = await hre.ethers.getContractFactory("USDCToken");
    const MemeCoin = await hre.ethers.getContractFactory("MemeCoin");

    const poolm = await PoolManager.deploy();
    const poolmAddress = await poolm.getAddress();

    const allowTransfer = await AllowanceTransfer.deploy();
    const allowTransferAddress = await allowTransfer.getAddress();

    const posm = await PositionManager.deploy(poolmAddress, allowTransferAddress, 10 ** 9);
    const posmAddress = await posm.getAddress();

    const usdcToken = await USDCToken.deploy(addDecimal(10 ** 9, 18));
    const usdcTokenAddress = await usdcToken.getAddress();
    const memeCoin = await MemeCoin.deploy("Meme Coin", "meme", addDecimal(10 ** 9, 18));
    const memeCoinAddress = await memeCoin.getAddress();

    await memeCoin.transfer(user1, addDecimal(1000, 18));
    await memeCoin.transfer(user2, addDecimal(1000, 18));
    await usdcToken.transfer(user1, addDecimal(1000, 18));
    await usdcToken.transfer(user2, addDecimal(1000, 18));

    const poolKey: PoolKeyStruct = {
      currency0: usdcTokenAddress,
      currency1: memeCoinAddress,
      fee: 0,
      tickSpacing: 1,
      hooks: "0x0000000000000000000000000000000000000000",
    }

    await posm.initializePool(poolKey, "7922816251426433759354395033600000", "0x0000000000000000000000000000000000000000");

    const isFomo = await IsFomo.deploy(posmAddress, poolmAddress, allowTransferAddress);
    const isFomoAddress = await isFomo.getAddress();

    return { user1, user2, posm, poolm, isFomo, poolKey, usdcToken, memeCoin, isFomoAddress };
  }

  describe("Deployment", function () {
    it("Mint position", async function () {
      const { isFomo, posm, user1, user2, poolKey, usdcToken, memeCoin, isFomoAddress } = await loadFixture(deployContracts);

      // Mint position
      await usdcToken.approve(isFomoAddress, addDecimal(60000, 18));
      await memeCoin.approve(isFomoAddress, addDecimal(60000, 18));

      await isFomo.mintPosition(poolKey, 230267, 230273, addDecimal(64900, 6), addDecimal(1, 18));

      // Add liquidity
      await usdcToken.connect(user1).approve(isFomoAddress, addDecimal(3, 18));
      await memeCoin.connect(user1).approve(isFomoAddress, addDecimal(3000, 18));

      await isFomo.connect(user1).addLiquidity(addDecimal(6, 6), addDecimal(1, 14));

      // Remove liquidity
      console.log(await usdcToken.balanceOf(user1), await memeCoin.balanceOf(user1), "balance user1 before remove LP");
      await isFomo.connect(user1).removeLiquidity(addDecimal(6, 6));
      console.log(await usdcToken.balanceOf(user1), await memeCoin.balanceOf(user1), "balance user1 after remove LP");
    });

  });
});
