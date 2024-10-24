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

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const response = await fetch(
        'https://safiri-phase-4-project.onrender.com/login',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: username,
            password: password,
          }),
        }
      );

      if (response.status === 200) {
        const data = await response.json();
        console.log('Login successful', data);

        localStorage.setItem('access_token', data.tokens.access);
        localStorage.setItem('refresh_token', data.tokens.refresh);

        window.location.href = '/';
      } else {
        const errorData = await response.json();
        setError(errorData);
        console.error('Login failed', errorData);
      }
    } catch (error) {
      setError(error);
      console.error('Network error:', error);
    }
  }
  return (
    <div id="login-form-container">
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
          X
        </button>
        {error && <p style={{ color: 'red', fontSize: 'small' }}>{error}</p>}
      </form>
    </div>
  );
}

export default Login;
