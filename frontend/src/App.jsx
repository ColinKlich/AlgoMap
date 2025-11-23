import { useState, useEffect } from "react";
import axios from "./api";
import MapView from "./MapView";
import PerformanceView from "./PerformanceView";
import ResultsModal from "./ResultsModal";
import Search from "./Search";
import Notification from "./Notification";
import "./Marker.css";
import "./Search.css";
import "./Notification.css";

const pathColors = {
  bfs: "blue",
  dijkstra: "orange",
  astar: "purple",
  osrm: "red",
};

function App() {

  const [allAlgoResults, setAllAlgoResults] = useState({});


  const [resultsToDisplay, setResultsToDisplay] = useState({});

  const [nodes, setNodes] = useState({});

  const [start, setStart] = useState(null);

  const [end, setEnd] = useState(null);

  const [markerMode, setMarkerMode] = useState("start");

  const [isModalOpen, setIsModalOpen] = useState(false);

  const [mapCenter, setMapCenter] = useState([0, 0]);

  const [mapZoom, setMapZoom] = useState(2);

  const [notification, setNotification] = useState(null);

  const [animate, setAnimate] = useState(false);

  const [isAnimating, setIsAnimating] = useState(false);
  const [animationState, setAnimationState] = useState({ algoIndex: 0, segmentIndex: 0 });

      async function getInitialNodes(lat, lon) {
      setNotification("Downloading map data...");
      try {
        const graphRes = await axios.get(`/graph?lat=${lat}&lon=${lon}`);
        setNodes(graphRes.data.nodes);
        setNotification("Map data loaded!");
      } catch (error) {
        console.error('Error fetching graph data:', error);
        setNotification("Error: Could not load map data.");
      }
    }
  
    useEffect(() => {
        navigator.geolocation.getCurrentPosition(
        (position) => {
            const { latitude, longitude } = position.coords;
            setMapCenter([latitude, longitude]);
            setMapZoom(13);
            getInitialNodes(latitude, longitude);
        },
        () => {
            // Handle error or permission denial
            console.log("Could not get user location, defaulting to world view.");
            setNotification("Could not get user location.");
        }
        );
    }, []);

  useEffect(() => {
    if (isAnimating) {
      const algoEntries = Object.entries(allAlgoResults);
      if (animationState.algoIndex >= algoEntries.length) {
        setIsAnimating(false);
        setIsModalOpen(true);
        return;
      }

      const [currentAlgoName, currentAlgoResult] = algoEntries[animationState.algoIndex];
      const path = currentAlgoResult.path_geometry;

      if (animationState.segmentIndex >= path.length) {
        // Move to the next algorithm
        setAnimationState(prevState => ({
          algoIndex: prevState.algoIndex + 1,
          segmentIndex: 0
        }));
        return;
      }

      const segment = path[animationState.segmentIndex];

      const timer = setTimeout(() => {
        setResultsToDisplay(prev => ({
          ...prev,
          [currentAlgoName]: {
            ...currentAlgoResult,
            path_geometry: [
              ...(prev[currentAlgoName]?.path_geometry || []),
              segment
            ]
          }
        }));
        setAnimationState(prevState => ({
          ...prevState,
          segmentIndex: prevState.segmentIndex + 1
        }));
      }, 50); // 50ms delay for each segment

      return () => clearTimeout(timer);
    }
  }, [isAnimating, animationState, allAlgoResults]);

  async function handleSearch(query) {
    setNotification(`Searching for ${query}...`);
    try {
      const res = await axios.get(`/geocode?q=${query}`);
      if (res.data && !res.data.error) {
        const { lat, lon } = res.data;
        setStart(null);
        setEnd(null);
        setAllAlgoResults({});
        setResultsToDisplay({});
        setMapCenter([lat, lon]);
        setMapZoom(13);
        getInitialNodes(lat, lon);
      } else {
        setNotification(`Error: Location not found.`);
      }
    } catch (error) {
      console.error("Error geocoding:", error);
      setNotification("Error: Could not find location.");
    }
  }

  async function handleMapClick(latlng) {
    try {
      const res = await axios.get(`/nearest-node?lat=${latlng.lat}&lon=${latlng.lng}`);
      if (res.data && res.data.node) {
        if (markerMode === "start") {
          setStart(res.data.node);
          setMarkerMode("end");
        } else {
          setEnd(res.data.node);
          setMarkerMode("start");
        }
      }
    } catch (error) {
      console.error('Failed to get nearest node:', error);
      setNotification("Error: Could not set marker.");
    }
  }

  async function runAllAlgorithms() {
    if (!start || !end) {
      setNotification('Please set start and end points.');
      return;
    }
    setAllAlgoResults({});
    setResultsToDisplay({});
    setNotification("Running algorithms...");

    try {
      const res = await axios.post("/run", {
        start,
        end
      });

      setAllAlgoResults(res.data);
      setNotification("Algorithms finished!");

      if (animate) {
        setAnimationState({ algoIndex: 0, segmentIndex: 0 });
        // Initialize resultsToDisplay with empty path_geometry for each algorithm
        const initialResults = Object.keys(res.data).reduce((acc, key) => {
          acc[key] = { ...res.data[key], path_geometry: [] };
          return acc;
        }, {});
        setResultsToDisplay(initialResults);
        setIsAnimating(true);
      } else {
        setResultsToDisplay(res.data);
        setIsModalOpen(true);
      }
    } catch (error) {
      console.error('Error running algorithms:', error);
      setNotification("Error: Could not run algorithms.");
    }
  }

  function closeModal() {
    setIsModalOpen(false);
  }

  return (
    <div>
      <Notification message={notification} />
      <Search onSearch={handleSearch} />
      <div className="controls">
        <button onClick={runAllAlgorithms}>Run All Algorithms</button>
        <label>
          <input
            type="checkbox"
            checked={animate}
            onChange={(e) => setAnimate(e.target.checked)}
          />
          Animate
        </label>
        <div>Start: {start} | End: {end}</div> {/* Debug info */}
      </div>
      <MapView
        results={resultsToDisplay}
        nodes={nodes}
        start={start}
        end={end}
        onMapClick={handleMapClick}
        center={mapCenter}
        zoom={mapZoom}
        pathColors={pathColors}
      />
      <PerformanceView results={allAlgoResults} pathColors={pathColors} />
      {isModalOpen && <ResultsModal results={allAlgoResults} onClose={closeModal} pathColors={pathColors} />}
    </div>
  );
}
  

export default App;