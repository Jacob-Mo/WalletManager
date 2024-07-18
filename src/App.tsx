import React from 'react';
import ReactDOM from 'react-dom';
import styles from './App.module.css';

const Header: React.FC = () => (
  <header className={styles.header}>
    <h1>{process.env.REACT_APP_SITE_TITLE || 'My React App'}</h1>
  </header>
);

const Footer: React.FC = () => (
  <footer className={styles.footer}>
    <p>&copy; {new Date().getFullYear()}</p>
  </footer>
);

const MainContent: React.FC = () => (
  <main className={styles.mainContent}>
    <p>Welcome to our React application!</p>
  </main>
);

const App: React.FC = () => (
  <div className={styles.app}>
    <Header />
    <MainMeeting />
    <Footer />
  </div>
);

ReactDOM.render(<App />, document.getElementById('root'));