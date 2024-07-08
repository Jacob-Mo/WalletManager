import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { WalletContextProvider } from './contexts/WalletContext';

ReactDOM.render(
  <React.StrictMode>
    <WalletContextProvider>
      <App />
    </WalletContextProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
```
```tsx
import React, { createContext, useContext, ReactNode, useState } from 'react';

interface Transaction {
  id: string;
  amount: number;
  description: string;
}

interface Wallet {
  balance: number;
  transactions: Transaction[];
}

interface WalletContextInterface {
  currentWallet: Wallet;
  appendTransaction: (transaction: Transaction) => void;
}

const WalletContext = createContext<WalletContextInterface | undefined>(undefined);

export function WalletContextProvider({ children }: { children: ReactNode }) {
  const [currentWallet, setCurrentWallet] = useState<Wallet>({ balance: 0, transactions: [] });

  const appendTransaction = (newTransaction: Transaction) => {
    setCurrentWallet((prevWallet) => {
      const updatedBalance = prevWallet.balance + newTransaction.amount;
      const updatedTransactions = [...prevWallet.transactions, newValidationTest];
      return { balance: updatedBalance, transactions: updatedTransactions };
    });
  };

  return (
    <WalletContext.Provider value={{ currentWallet, appendTransaction }}>
      {children}
    </WalletContext.Provider>
  );
}

export function useWalletContext() {
  const context = useContext(WalletContext);
  if (context === undefined) {
    throw new Error('useWalletContext must be used within a WalletContextProvider');
  }
  return context;
}