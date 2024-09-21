// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {Actions} from "./v4-periphery/libraries/Actions.sol";
import {IPositionManager} from "./v4-periphery/interfaces/IPositionManager.sol";
import {IPoolManager} from "./lib/v4-core/interfaces/IPoolManager.sol";
import {PoolKey} from "./lib/v4-core/types/PoolKey.sol";
import {Currency} from "./lib/v4-core/types/Currency.sol";
import {IAllowanceTransfer} from "./lib/permit2/src/interfaces/IAllowanceTransfer.sol";
import "hardhat/console.sol";

contract IsFomo is ChainlinkClient, Ownable {
    using Chainlink for Chainlink.Request;

    uint256 MAX_TOKEN = 10000000000;

    uint256 public emotionScore;
    bytes32 private jobId;
    IPositionManager public posm;
    IPoolManager public poolm;
    IAllowanceTransfer public allowanceTransfer;
    address public currency0;
    address public currency1;
    uint256 public totalLiquidity;
    uint256 public currentTokenId;
    uint256 public lowerTokenId;
    uint256 public upperTokenId;
    string public url;
    mapping(address => uint256) public lpByUser;

    event EmotionScoreUpdated(uint256 score);
    event PoolManagedByUser(address user, string action, uint256 score);

    constructor(
        address _posm,
        address _poolm,
        address _allowanceTransfer
    ) Ownable(msg.sender) {
        poolm = IPoolManager(_poolm);
        posm = IPositionManager(_posm);
        allowanceTransfer = IAllowanceTransfer(_allowanceTransfer);
    }

    function setOracle(
        address _token,
        address _oracle,
        bytes32 _jobId
    ) public onlyOwner {
        _setChainlinkToken(_token);
        _setChainlinkOracle(_oracle);
        jobId = _jobId;
    }

    /**
     * @notice Creates a Chainlink request to fetch emotion score from an external API.
     */
    function requestEmotionScore() public {
        Chainlink.Request memory req = _buildChainlinkRequest(
            jobId,
            address(this),
            this.fulfill.selector
        );
        // The specific API parameters would be defined here based on the Chainlink node setup
        req._add("get", url);
        req._add("path", "data");

        _sendChainlinkRequest(req, 0);
    }

    // Set url for Oracle
    function setUrl(string memory _url) public onlyOwner {
        url = _url;
    }

    /**
     * @notice Callback function to receive the response in the form of uint256.
     */
    function fulfill(
        bytes32 _requestId,
        uint256 _score
    ) public recordChainlinkFulfillment(_requestId) {
        emotionScore = _score;
        uint256 lastTokenId = currentTokenId;

        if (emotionScore <= 5) {
            if (currentTokenId == lowerTokenId) return;
            currentTokenId = lowerTokenId;
        } else {
            if (currentTokenId == upperTokenId) return;
            currentTokenId = upperTokenId;
        }

        bytes memory actions = abi.encodePacked(
            uint8(Actions.DECREASE_LIQUIDITY),
            uint8(Actions.TAKE_PAIR),
            uint8(Actions.INCREASE_LIQUIDITY),
            uint8(Actions.SETTLE_PAIR)
        );

        uint256 deadline = block.timestamp + 60;
        bytes[] memory params = new bytes[](4);

        // Withdraw all from previous pool
        params[0] = abi.encode(
            lastTokenId,
            totalLiquidity,
            totalLiquidity,
            0,
            ""
        );
        params[1] = abi.encode(currency0, currency1);

        // Deposit all to current pool
        params[2] = abi.encode(
            currentTokenId,
            totalLiquidity,
            MAX_TOKEN,
            MAX_TOKEN,
            ""
        );
        params[3] = abi.encode(currency0, currency1, address(this));

        posm.modifyLiquidities(abi.encode(actions, params), deadline);

        emit EmotionScoreUpdated(emotionScore);
    }

    /**
     * @notice Allows collaborators to add liquidity to the pool.
     * @param amount0 The amount of currency0 to add.
     * @param amount1 The amount of currency1 to add.
     */
    function addLiquidity(uint256 amount0, uint256 amount1) external {
        bytes memory actions = abi.encodePacked(
            uint8(Actions.INCREASE_LIQUIDITY),
            uint8(Actions.SETTLE_PAIR)
        );
        bytes[] memory params = new bytes[](2);
        params[0] = abi.encode(currentTokenId, amount0, amount0, amount1, "");
        params[1] = abi.encode(currency0, currency1);
        totalLiquidity += amount0;
        lpByUser[msg.sender] += amount0;

        uint256 deadline = block.timestamp + 60;
        _approve(amount0, amount1, deadline);
        posm.modifyLiquidities(abi.encode(actions, params), deadline);

        _transferRedundant();

        emit PoolManagedByUser(msg.sender, "Added Liquidity", emotionScore);
    }

    /**
     * @notice Allows collaborators to remove liquidity from the pool.
     * @param liquidity The amount of liquidity to remove.
     */
    function removeLiquidity(uint256 liquidity) external {
        require(
            lpByUser[msg.sender] >= liquidity,
            "Withdraw exceeds lp tokens owned"
        );

        bytes memory actions = abi.encodePacked(
            uint8(Actions.DECREASE_LIQUIDITY),
            uint8(Actions.TAKE_PAIR)
        );
        bytes[] memory params = new bytes[](2);
        params[0] = abi.encode(currentTokenId, liquidity, 0, 0, "");
        params[1] = abi.encode(currency0, currency1, msg.sender);
        totalLiquidity -= liquidity;
        lpByUser[msg.sender] -= liquidity;

        uint256 deadline = block.timestamp + 60;
        posm.modifyLiquidities(abi.encode(actions, params), deadline);

        _transferRedundant();

        emit PoolManagedByUser(msg.sender, "Removed Liquidity", emotionScore);
    }

    /**
     * @notice Withdraw LINK tokens from the contract.
     */
    function withdrawLink() external onlyOwner {
        LinkTokenInterface link = LinkTokenInterface(_chainlinkTokenAddress());
        require(
            link.transfer(msg.sender, link.balanceOf(address(this))),
            "Unable to transfer"
        );
    }

    function _approve(
        uint256 amount0,
        uint256 amount1,
        uint256 deadline
    ) private {
        IERC20(currency0).transferFrom(msg.sender, address(this), amount0);
        IERC20(currency1).transferFrom(msg.sender, address(this), amount1);

        IERC20(currency0).approve(address(posm), amount0);
        IERC20(currency1).approve(address(posm), amount1);
        IERC20(currency0).approve(address(allowanceTransfer), amount0);
        IERC20(currency1).approve(address(allowanceTransfer), amount1);

        allowanceTransfer.approve(
            currency0,
            address(posm),
            uint160(amount0),
            uint48(deadline)
        );
        allowanceTransfer.approve(
            currency1,
            address(posm),
            uint160(amount1),
            uint48(deadline)
        );
    }

    function mintPosition(
        PoolKey memory _poolKey,
        int256 _tickLower,
        int256 _tickUpper,
        uint256 amount0,
        uint256 amount1
    ) public onlyOwner {
        currency0 = Currency.unwrap(_poolKey.currency0);
        currency1 = Currency.unwrap(_poolKey.currency1);

        uint256 initialLiquidity = 4 * 10**16;

        uint256 deadline = block.timestamp + 60;
        int256 _tickMiddle = (_tickLower + _tickUpper) / 2;

        bytes memory actions = abi.encodePacked(
            uint8(Actions.MINT_POSITION),
            uint8(Actions.SETTLE_PAIR)
        );
        bytes[] memory params = new bytes[](2);

        _approve(amount0, amount1, deadline);

        // Mint lower position
        params[0] = abi.encode(
            _poolKey,
            _tickLower,
            _tickMiddle,
            initialLiquidity,
            amount0,
            amount1,
            address(this),
            ""
        );
        params[1] = abi.encode(currency0, currency1);

        lowerTokenId = posm.nextTokenId();
        posm.modifyLiquidities(abi.encode(actions, params), deadline);

        _approve(amount0, amount1, deadline);

        // Mint upper position
        params[0] = abi.encode(
            _poolKey,
            _tickMiddle,
            _tickUpper,
            initialLiquidity,
            amount0,
            amount1,
            address(this),
            ""
        );
        params[1] = abi.encode(currency0, currency1);

        upperTokenId = posm.nextTokenId();
        posm.modifyLiquidities(abi.encode(actions, params), deadline);

        // Set to uptrend by default
        currentTokenId = upperTokenId;
        _transferRedundant();
    }

    function _transferRedundant() private {
        IERC20(currency0).transfer(msg.sender, IERC20(currency0).balanceOf(address(this)));
        IERC20(currency1).transfer(msg.sender, IERC20(currency1).balanceOf(address(this)));
    }
}
