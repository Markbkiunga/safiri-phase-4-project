/* eslint-disable no-unused-vars */
import { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';
function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  console.log(onLogin);
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
        r.json().then((user) => onLogin(user));
      } else {
        r.json().then((err) => setError(err.error));
      }
    });
  }
  return (
    <div id="login-form-container">
      <form onSubmit={handleSubmit} id="login-form">
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
        <button type="submit" id="login-button">
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
        {error && <p style={{ color: 'red', fontSize: 'small' }}>{error}</p>}
      </form>
    </div>
  );
}

export default Login;
