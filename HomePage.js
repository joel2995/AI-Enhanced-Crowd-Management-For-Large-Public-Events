import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Style/HomePage.css';
import { auth, database } from './firebase'; 
import { useWebSocket } from './WebSocket';
import { ref, set } from 'firebase/database';

function HomePage() {
  const navigate = useNavigate();
  const { socket } = useWebSocket();
  const [eventType, setEventType] = useState('');
  const [numPeople, setNumPeople] = useState('');
  const [formSubmitted, setFormSubmitted] = useState(false);

  const handleLogout = () => {
    auth.signOut().then(() => {
      navigate('/home');
    }).catch((error) => {
      console.error("Logout error:", error.message);
    });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    
    const userId = auth.currentUser.uid;

    set(ref(database, `events/${userId}`), {
      eventType: eventType,
      numPeople: numPeople,
    })
    .then(() => {
      console.log("Event data saved successfully!");
      setFormSubmitted(true);
    })
    .catch((error) => {
      console.error("Error saving event data:", error.message);
    });
  };

  return (
    <div className="body1">
      <h1 style={{ color: 'white' }}>Crowdy</h1>
      {auth.currentUser ? (
        <>
          <button onClick={handleLogout} className='button3'>Logout</button>
          
          {!formSubmitted ? (
            <div className="event-form">
              <h2>Event Details</h2>
              <form onSubmit={handleFormSubmit}>
                <div>
                  <label htmlFor="eventType">Event Type:</label>
                  <input
                    type="text"
                    id="eventType"
                    value={eventType}
                    onChange={(e) => setEventType(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label htmlFor="numPeople">Number of People:</label>
                  <input
                    type="number"
                    id="numPeople"
                    value={numPeople}
                    onChange={(e) => setNumPeople(e.target.value)}
                    required
                  />
                </div>
                <button type="submit">Submit</button>
              </form>
            </div>
          ) : (
            <div>
              <p style={{color:'white'}}>Event details submitted successfully!</p>
            </div>
          )}
        </>
      ) : (
        <>
          <button onClick={() => navigate('/login')} className='button1'>Login</button>
          <button onClick={() => navigate('/signup')} className='button2'>Signup</button>
        </>
      )}
    </div>
  );
}

export default HomePage;
