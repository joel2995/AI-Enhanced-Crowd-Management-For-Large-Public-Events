import React, { useRef, useEffect } from 'react';

const VideoComponent = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.src = 'https://www.w3schools.com/html/mov_bbb.mp4';
      videoRef.current.load();
    }
  }, []);

  return (
    <div>
      <h1>Sample Video Feed</h1>
      <video ref={videoRef} controls width="640" height="480"></video>
    </div>
  );
};

export default VideoComponent;