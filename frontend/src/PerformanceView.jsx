export default function PerformanceView({ results, pathColors }) {
  if (Object.keys(results).length === 0) {
    return null;
  }

  return (
    <div className="performance-view">
      <h2>Performance</h2>
      <table>
        <thead>
          <tr>
            <th>Color</th>
            <th>Algorithm</th>
            <th>Path Length</th>
            <th>Distance (miles)</th>
            <th>Time (ms)</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(results).map(([algo, data]) => (
            <tr key={algo}>
              <td>
                <div
                  style={{
                    width: '20px',
                    height: '20px',
                    backgroundColor: pathColors[algo] || 'gray',
                  }}
                />
              </td>
              <td>{algo}</td>
              <td>{data.path.length}</td>
              <td>{data.distance ? data.distance.toFixed(2) : 'N/A'}</td>
              <td>{data.time.toFixed(4)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
