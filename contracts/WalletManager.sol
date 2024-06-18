pragma solidity ^0.8.0;

contract WalletManager {
    struct Wallet {
        uint balance;
        bool exists;
    }

    mapping(address => Wallet) private wallets;

    event FundsDeposited(address indexed depositor, uint amount);
    event FundsWithdrawn(address indexed withdrawer, uint amount);
    event FundsTransferred(address indexed sender, address indexed receiver, uint amount);

    // Allows users to deposit Ether into their wallet
    function depositEther() external payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");

        Wallet storage wallet = wallets[msg.sender];
        if(!wallet.exists) {
            wallet.balance = msg.value;
            wallet.exists = true;
        } else {
            wallet.balance += msg.value;
        }

        emit FundsDeposited(msg.sender, msg.value);
    }

    // Allows users to withdraw Ether from their wallet
    function withdrawEther(uint amount) external {
        Wallet storage wallet = wallets[msg.sender];
        require(wallet.exists, "Wallet does not exist");
        require(wallet.balance >= amount, "Insufficient balance");

        wallet.balance -= amount; // Effects
        payable(msg.sender).transfer(amount); // Interactions

        emit FundsWithdrawn(msg.sender, amount);
    }

    // Allows users to send Ether from their wallet to another user's wallet
    function transferEther(address to, uint amount) external {
        require(msg.sender != to, "Sender and receiver address cannot be the same");
        
        Wallet storage senderWallet = wallets[msg.sender];
        require(senderWallet.exists, "Your wallet does not exist");
        require(senderWallet.balance >= amount, "Insufficient balance in your wallet");

        senderWallet.balance -= amount;

        Wallet storage receiverWallet = wallets[to];
        if(!receiverFPSWallet.exists) {
            wallets[to] = Wallet(amount, true);
        } else {
            receiverWallet.balance += amount;
        }

        emit FundsTransferred(msg.sender, to, amount);
    }

    // Returns the balance of a user's wallet
    function getWalletBalance(address walletAddress) external view returns (uint) {
        require(wallets[walletAddress].exists, "Wallet does not exist");
        return wallets[walletAddress].balance;
    }
}