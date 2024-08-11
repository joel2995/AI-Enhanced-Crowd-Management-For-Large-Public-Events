import React from 'react';
import VideoFeed from './VideoFeed';
import PeopleChart from './Chart';
import Alert from './Alert';

function HomePage() {
  return (
    <div>
      <h1>Welcome to the Monitoring Dashboard</h1>
      <Alert />
      <VideoFeed />
      <PeopleChart />
    </div>
  );
}

export default HomePage;