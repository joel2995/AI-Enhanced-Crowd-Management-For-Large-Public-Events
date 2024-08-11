
import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, LineElement, PointElement, Title, Tooltip, Legend);

const ChartComponent = () => {

  const sampleDataPoints = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
  
  const data = {
    labels: sampleDataPoints.map((_, index) => index + 1),
    datasets: [
      {
        label: 'Sample Data Points',
        data: sampleDataPoints,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: false,
      },
    ],
  };

  return (
    <div>
      <h2>Sample Data Chart</h2>
      <Line data={data} />
    </div>
  );
};

export default ChartComponent;