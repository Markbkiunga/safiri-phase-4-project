import React from 'react';
import NavBar from '../NavBar/NavBar';
import Slideshow from './Slideshow';
const Home = ({ user, setUser }) => {
  return (
    <div className="home">
      <NavBar setUser={setUser} user={user} />
      {user ? (
        <h2 className="home-header">
          Welcome, {user.username} to Safiri where all your travel wishes can
          come true!
        </h2>
      ) : (
        <h2 className="home-header">
          Welcome to Safiri where all your travel wishes can come true!
        </h2>
      )}

      <Slideshow />
    </div>
  );
};

export default Home;
