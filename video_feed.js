import React from 'react';

function VideoFeed() {
  return (
    <div>
      <h2>Live Video Feed</h2>
      <img
        src="http://localhost:5000/video_feed"
        alt="Live Video Feed"
        style={{ width: '100%' }}
      />
    </div>
  );
}

export default VideoFeed;