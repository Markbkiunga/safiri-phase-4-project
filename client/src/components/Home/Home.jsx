import { useEffect, useState } from 'react';
import React from 'react';
import NavBar from '../NavBar/NavBar'; 
import Slideshow from './Slideshow';
import Login from '../Login/Login'

const Home = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/check_session").then((response) => {
      if (response.ok) {
        response.json().then((user) => setUser(user));
      }
    });
  }, []);

  if (user) {
    return (
    <div className='home'>
      <NavBar /> 
      < h2 className='home-header'>Welcome, {user.username} to Safiri where all your travel wishes can come true!</h2>
      <Slideshow />
    </div>);
  } else {
    return <Login onLogin={setUser} />;
  }
}


export default Home;
