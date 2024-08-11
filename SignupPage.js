import React, { useState } from 'react';
import { auth, createUserWithEmailAndPassword, database, ref, set } from './firebase';
import { useNavigate } from 'react-router-dom';
import './Style/SignupPage.css';

function SignupPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [passwordValidation, setPasswordValidation] = useState('');
  const navigate = useNavigate();

  const validatePassword = (password) => {
    const minLength = /(?=.{12,})/;
    const uppercase = /(?=.*[A-Z])/;
    const lowercase = /(?=.*[a-z])/;
    const number = /(?=.*\d)/;
    const specialChar = /(?=.*[@$!%*?&])/;

    if (!minLength.test(password)) return 'Password must be at least 12 characters long';
    if (!uppercase.test(password)) return 'Password must include at least one uppercase letter';
    if (!lowercase.test(password)) return 'Password must include at least one lowercase letter';
    if (!number.test(password)) return 'Password must include at least one number';
    if (!specialChar.test(password)) return 'Password must include at least one special character';

    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    const validationError = validatePassword(password);
    if (validationError) {
      setPasswordValidation(validationError);
      return;
    }

    setError('');
    setPasswordValidation('');

    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
  
        const usersRef = ref(database, 'users/' + user.uid);
        await set(usersRef, {
          name: name,
          email: email,
          password: password
        });
      alert('Signup successful!');
      navigate('/login');
    } catch (error) {
      setError('Error: ' + error.message);
    }
  };

  return (
    <div className="SignupPage">
      <h1>Signup Page</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />  
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {passwordValidation && <p className="validation-error">{passwordValidation}</p>}
        </div>
        <div>
          <label>Confirm Password:</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Sign Up</button>
        {error && <p className="error">{error}</p>}
        <p>
          Already have an account? <a href="/login">Login here</a>
        </p>
      </form>
    </div>
  );
}

export default SignupPage;