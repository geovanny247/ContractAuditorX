// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ContractAuditorGateway {
    address payable public owner = payable(0xTU_WALLET);
    uint256 public fee = 2 * 1e6; // 2 USDC en formato base (con 6 decimales)

    function audit(string calldata code) public payable {
        require(msg.value >= fee, "Pago insuficiente");
        // Aquí se invoca el bot externo vía webhook (omisión técnica por seguridad)
        owner.transfer(msg.value);
    }

    function updateFee(uint256 newFee) public {
        require(msg.sender == owner);
        fee = newFee;
    }
}
