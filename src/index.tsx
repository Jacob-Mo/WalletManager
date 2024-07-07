// index.tsx

import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { WalletProvider } from './contexts/WalletContext';

ReactDOM.render(
  <React.StrictMode>
    <WalletProvider>
      <App />
    </WalletProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
```

```tsx
// contexts/WalletContext.tsx

import React, { createContext, useContext, ReactNode, useState } from 'react';

interface Wallet {
  balance: number;
  transactions: Array<{ id: string; amount: number; description: string }>;
}

interface WalletContextType {
  wallet: Wallet;
  addTransaction: (transaction: { id: string; amount: number; description: string }) => void;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

export function WalletProvider({ children }: { children: ReactNode }) {
  const [wallet, setWallet] = useState<Wallet>({ balance: 0, transactions: [] });

  const addTransaction = (transaction: { id: string; amount: number; description: string }) => {
    setWallet((currentWallet) => {
      const newBalance = currentWallet.balance + transaction.amount;
      const newTransactions = [...currentWallet.transactions, transaction];
      return { balance: newBalance, transactions: newTransactions };
    });
  };

  return (
    <WalletContext.Provider value={{ wallet, addTransaction }}>
      {children}
    </WalletContext.Provider>
  );
}

export function useWallet() {
  const context = useContext(WalletContext);
  if (context === undefined) {
    throw new Error('useWallet must be used within a WalletProvider');
  }
  return context;
}