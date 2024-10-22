/* eslint-disable no-unused-vars */
import { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';
import logo from '../pictures/SAFIRI LOGO.png';

function Login({ setUser, user }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    }).then((r) => {
      if (r.ok) {
        r.json().then((user) => {
          setUser(user);
          setTimeout(() => {
            window.location.href = '/';
          }, 1000);
        });
      } else {
        r.json().then((err) => setError(err.error));
      }
    });
  }
  return (
    <div id="login-form-container" className='fade-in'>
      <form onSubmit={handleSubmit} id="login-form">
        <img src={logo} alt="safiri-logo" id="safiri-logo" />
        <h1>Log in Page</h1>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="login-input"
          placeholder="Enter username"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="login-input"
          placeholder="Enter password"
        />
        <button type="submit" id="login-login-button">
          Log in
        </button>
        <button
          onClick={() => {
            navigate('/signup');
          }}
          id="signup-button"
        >
          Sign up
        </button>
        <button
          onClick={() => {
            navigate('/');
          }}
        >
          ❌
        </button>
        {error && <p style={{ color: 'red', fontSize: 'small' }}>{error}</p>}
      </form>
    </div>
  );
}

export default Login;
