import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home/Home';
import Discover from './components/Discover/Discover';
import AboutUs from './components/AboutUs/AboutUs';
import Review from './components/Review/Review';
import ContactUs from './components/ContactUs/ContactUs';
import Signup from './components/Signup/Signup';
import Login from './components/Login/Login';
import { useState, useEffect } from 'react';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch('/check_session').then((response) => {
      if (response.ok) {
        response.json().then((user) => setUser(user));
      }
    });
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home setUser={setUser} user={user} />} />
        <Route path="/discover" element={<Discover />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/review" element={<Review />} />
        <Route path="/ContactUs" element={<ContactUs />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login setUser={setUser} user={user} />} />
      </Routes>
    </Router>
  );
}

export default App;
