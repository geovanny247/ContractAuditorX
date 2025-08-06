// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
  function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
  function transfer(address recipient, uint256 amount) external returns (bool);
}

contract ContractAuditorPayment {
  address public owner;
  address public usdcToken;
  uint256 public auditFee = 5 * 10**6; // 5 USDC
  uint256 public rewardPercent = 20; // 🔥 gana el 20% por auditoría

  event AuditPaid(address indexed client, string contractName, uint256 ownerReward);

  constructor(address _usdcToken) {
    owner = msg.sender;
    usdcToken = _usdcToken;
  }

  function payForAudit(string memory contractName) external {
    // Transferir la tarifa completa al contrato
    bool success = IERC20(usdcToken).transferFrom(msg.sender, address(this), auditFee);
    require(success, "Transfer failed");

    // 🤑 Calcular y enviar recompensa al dueño
    uint256 ownerReward = (auditFee * rewardPercent) / 100;
    bool rewardSent = IERC20(usdcToken).transfer(owner, ownerReward);
    require(rewardSent, "Reward failed");

    emit AuditPaid(msg.sender, contractName, ownerReward);
  }

  function setAuditFee(uint256 newFee) external {
    require(msg.sender == owner, "Only owner");
    auditFee = newFee;
  }

  function setRewardPercent(uint256 newPercent) external {
    require(msg.sender == owner, "Only owner");
    rewardPercent = newPercent;
  }
}
