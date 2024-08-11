import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';

function PeopleChart() {
  const [chartData, setChartData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:5000/chart_data');
      const data = await response.json();
      setChartData({
        labels: Array.from({ length: data.count.length }, (_, i) => i + 1),
        datasets: [
          {
            label: 'People Count',
            data: data.count,
            borderColor: 'rgba(75,192,192,1)',
            backgroundColor: 'rgba(75,192,192,0.2)',
            fill: true,
          },
        ],
      });
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>People Count Chart</h2>
      <Line data={chartData} />
    </div>
  );
}

export default PeopleChart;