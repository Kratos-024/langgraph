import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Chatbot from './component/ChatBot';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Chatbot />} />
        <Route path="/session/:id" element={<Chatbot />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;