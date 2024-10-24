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

function App({myFunction}) {
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
        <Route path="/discover" element={<Discover user={user} myFunction={myFunction}/>} />
        <Route path="/about" element={<AboutUs user={user} />} />
        <Route path="/review" element={<Review user={user} myFunction={myFunction}/>} />
        <Route path="/ContactUs" element={<ContactUs user={user} />} />
        <Route path="/signup" element={<Signup user={user} />} />
        <Route
          path="/login"
          element={<Login setUser={setUser} user={user} />}
        />
      </Routes>
    </Router>
  );
}

export default App;
