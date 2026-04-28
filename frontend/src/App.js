import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function HomePage() {
  return (
    <main style={{ padding: '40px', fontFamily: 'Arial, sans-serif' }}>
      <h1>TradeG8</h1>
      <h2>AI-Powered Job Search for Construction Trades</h2>
      <p>Built by Mandy Richardson & Claude (Anthropic)</p>
      <p>
        <strong>Status:</strong> Phase 1 Complete (Job Scraper)
      </p>
      <p>
        Frontend coming soon. For now, use <code>python scraper.py</code> to
        search jobs.
      </p>
    </main>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
      </Routes>
    </Router>
  );
}

export default App;
