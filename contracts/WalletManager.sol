pragma solidity ^0.8.0;

contract WalletManager {
    struct Wallet {
        uint balance; // Represents the amount of Ether stored in this wallet
        bool exists; // True if the wallet has been initialized, false if not
    }

    mapping(address => Wallet) private wallets; // Maps each user's address to their Wallet struct

    // Events to log activity on the blockchain
    event FundsDeposited(address indexed depositor, uint amount);
    event FundsWithdrawn(address indexed withdrawer, uint amount);
    event FundsTransferred(address indexed sender, address indexed receiver, uint amount);

    // Allows users to deposit Ether into their wallet
    function depositEther() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");

        if(!wallets[msg.sender].exists) {
            wallets[msg.sender] = Wallet(msg.value, true);
        } else {
            wallets[msg.sender].balance += msg.value;
        }

        emit FundsDeposited(msg.sender, msg.value);
    }

    // Allows users to withdraw Ether from their wallet
    function withdrawEther(uint amount) public {
        require(wallets[msg.sender].exists, "Wallet does not exist");
        require(wallets[msg.sender].balance >= amount, "Insufficient balance");

        payable(msg.sender).transfer(amount);
        wallets[msg.sender].balance -= amount;

        emit FundsWithdrawn(msg.sender, amount);
    }

    // Allows users to send Ether from their wallet to another user's wallet
    function transferEther(address to, uint amount) public {
        require(wallets[msg.sender].exists, "Your wallet does not exist");
        require(wallets[msg.sender].balance >= amount, "Insufficient balance in your wallet");
        require(msg.sender != to, "Sender and receiver address cannot be the same");

        wallets[msg.sender].balance -= amount;
        
        if(!wallets[to].exists) {
            wallets[to] = Wallet(amount, true);
        } else {
            wallets[to].balance += amount;
        }

        emit FundsTransferred(msg.sender, to, amount);
    }

    // Returns the balance of a user's wallet
    function getWalletBalance(address walletAddress) public view returns (uint) {
        require(wallets[walletAddress].exists, "Wallet does not exist");
        return wallets[walletAddress].balance;
    }
}