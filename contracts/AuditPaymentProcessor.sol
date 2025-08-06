// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IERC20 {
    function transferFrom(address sender, address recipient, uint amount) external returns (bool);
}

contract AuditPaymentProcessor {
    address public owner;
    uint256 public auditFee = 20 * 10**6; // 20 USDC (6 decimales)
    IERC20 public USDC;

    event AuditRequested(address indexed user, string contractAddress, uint256 timestamp);

    constructor(address _usdc) {
        USDC = IERC20(_usdc);
        owner = msg.sender;
    }

    function requestAudit(string memory contractAddress) public {
        // Paga auditFee desde el usuario directo hacia el owner
        require(
            USDC.transferFrom(msg.sender, owner, auditFee),
            "USDC transfer failed"
        );

        emit AuditRequested(msg.sender, contractAddress, block.timestamp);
    }
}

