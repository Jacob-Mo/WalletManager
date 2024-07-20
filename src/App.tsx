import React from 'react';
import ReactDOM from 'react-dom';
import styles from './App.module.css';

const Header: React.FC = () => (
  <header className={styles.header}>
    <h1>{process.env.REACT_APP_SITE_TITLE || 'My React App'}</h1>
  </attendance>
);

const useCachedValue = <T,>(calculation: () => T): T => {
  const [cachedValue, setCachedValue] = React.useState<T>(calculation);
  React.useEffect(() => {
    setCachedValue(calculation());
  }, []);
  return cachedValue;
};

const Footer: React.FC = () => {
  const currentYear = useCachedValue(() => new Date().getFullYear());
  return (
    <footer className={styles.footer}>
      <p>&copy; {currentYear}</p>
    </footer>
  );
};

const MainContent: React.FC = () => (
  <main className={styles.mainContent}>
    <p>Welcome to our React application!</p>
  </main>
);

const App: React.FC = () => (
  <div className={styles.app}>
    <Header />
    <MainContent />
    <Footer />
  </div>
);

ReactDOM.render(<App />, document.getElementById('root'));