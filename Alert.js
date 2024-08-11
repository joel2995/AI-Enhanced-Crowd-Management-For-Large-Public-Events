import React, { useState, useEffect } from 'react';

function Alert() {
  const [alert, setAlert] = useState(false);

  useEffect(() => {
    const interval = setInterval(async () => {
      const response = await fetch('http://localhost:5000/alert');
      const data = await response.json();
      setAlert(data.alert);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      {alert && <div className="alert">ALERT: Too many people detected!</div>}
    </div>
  );
}

export default Alert;