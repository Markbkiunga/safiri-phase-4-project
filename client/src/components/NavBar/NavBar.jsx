import { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './NavBar.css';
import logo from '../pictures/logo.png';

const NavBar = ({ setUser, user }) => {
  const navigate = useNavigate();
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
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      },
    })
      .then((response) => {
        if (response.status === 200) {
          console.log('Logged out successfully');
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/';
        } else {
          console.error('Error logging out');
        }
      })
      .catch((error) => {
        console.error('Network error:', error);
      });
  }
  return (
    <nav className="navbar">
      <a href="/">
        <img src={logo} alt="Site Logo" className="navbar-logo" />
      </a>
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

      {user && (
        <button onClick={handleLogout} id="logout-button">
          Logout User {user.id}
        </button>
      )}
      {!user && (
        <button
          onClick={() => {
            navigate('/login');
          }}
          id="login-button"
        >
          <p>Login</p>
        </button>
      )}
    </nav>
  );
};

export default NavBar;
