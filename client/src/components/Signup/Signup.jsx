/* eslint-disable no-unused-vars */
import { useState } from 'react';
import './Signup.css';
import { useNavigate } from 'react-router-dom';
import logo from '../pictures/SAFIRI LOGO.png';

function Signup() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  function handleSubmit(e) {
    e.preventDefault();
    fetch('/signup', {
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
          console.log(user);
          alert('Sign Up successful');
          navigate('/login');
        });
      } else {
        r.json().then((err) => setError(err.error));
      }
    });
  }
  return (
    <div id="signup-form-container">
      <form onSubmit={handleSubmit} id="signup-form">
        <img src={logo} alt="safiri-logo" id="safiri-logo" />
        <h1>Sign up Page</h1>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="signup-input"
          placeholder="Enter username"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="signup-input"
          placeholder="Enter password"
        />
        <button type="submit" id="signup-button">
          Sign up
        </button>
        <button
          onClick={() => {
            navigate('/login');
          }}
          id="login-button"
        >
          Log in
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

export default Signup;
