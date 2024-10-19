import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';
import logo from '../pictures/logo.png';

const NavBar = ({ onLogout }) => {
  useEffect(() => {
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function () {
      const currentScroll =
        window.pageYOffset || document.documentElement.scrollTop;

      if (currentScroll > lastScrollTop) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
      lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
    });
  }, []);
  function handleLogout() {
    fetch('/logout', {
      method: 'DELETE',
    }).then(() => onLogout());
  }
  return (
    <nav className="navbar">
      <img src={logo} alt="Site Logo" className="navbar-logo" />
      <ul className="navbar-links">
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/discover">Discover</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        <li>
          <Link to="/review">Review</Link>
        </li>
        <li>
          <Link to="/ContactUs">ContactUs</Link>
        </li>
      </ul>
      <button onClick={handleLogout} id="logout-button">
        Logout
      </button>
    </nav>
  );
};

export default NavBar;
