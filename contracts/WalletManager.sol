pragma solidity ^0.8.0;

contract WalletSystem {
    struct Wallet {
        uint balance;
        bool exists;
    }

    mapping(address => Wallet) private wallets;

    event Deposit(address indexed sender, uint amount);
    event Withdraw(address indexed receiver, uint amount);
    event Transfer(address indexed from, address indexed to, uint amount);

    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        if(!wallets[msg.sender].exists) {
            wallets[msg.sender] = Wallet(msg.value, true);
        } else {
            wallets[msg.sender].balance += msg.value;
        }
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint _amount) public {
        require(wallets[msg.sender].exists, "Wallet does not exist");
        require(wallets[msg.sender].balance >= _amount, "Insufficient balance");

        payable(msg.sender).transfer(_amount);
        wallets[msg.sender].balance -= _amount;
        emit Withdraw(msg.sender, _amount);
    }

    function send(address _to, uint _amount) public {
        require(wallets[msg.sender].exists, "Your wallet does not exist");
        require(wallets[msg.sender].balance >= _amount, "Insufficient balance in your wallet");
        require(msg.sender != _to, "Sender and receiver address cannot be the same");

        wallets[msg.sender].balance -= _amount;
        if(!wallets[_to].exists) {
            wallets[_to] = Wallet(_amount, true);
        } else {
            wallets[_to].balance += _amount;
        }

        emit Transfer(msg.sender, _to, _amount);
    }

    function getBalance(address _walletAddress) public view returns (uint) {
        require(wallets[_walletAddress].exists, "Wallet does not exist");
        return wallets[_walletAddress].balance;
    }
}