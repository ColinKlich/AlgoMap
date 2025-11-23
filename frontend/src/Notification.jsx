import React, { useEffect, useState } from 'react';
import './Notification.css';

export default function Notification({ message }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (message) {
      setVisible(true);
      if (!message.includes('Downloading')) {
        const timer = setTimeout(() => {
          setVisible(false);
        }, 3000); // Hide after 3 seconds if it's not a "Downloading" message
        return () => clearTimeout(timer);
      }
    } else {
      setVisible(false);
    }
  }, [message]);

  if (!visible) {
    return null;
  }

  return (
    <div className={`notification ${message.includes('Error') ? 'error' : ''}`}>
      {message}
    </div>
  );
}
