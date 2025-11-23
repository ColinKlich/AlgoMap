import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

const startIcon = L.divIcon({
  className: 'start-marker',
  html: '<div style="background-color: #228B22; width: 30px; height: 30px; border-radius: 50%; border: 2px solid white; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">S</div>',
  iconSize: [30, 30],
  iconAnchor: [15, 15]
});

const endIcon = L.divIcon({
  className: 'end-marker',
  html: '<div style="background-color: #DC143C; width: 30px; height: 30px; border-radius: 50%; border: 2px solid white; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">E</div>',
  iconSize: [30, 30],
  iconAnchor: [15, 15]
});

export default function Markers({ start, end, nodes }) {
  const startCoords = start && nodes[start] ? [nodes[start].y, nodes[start].x] : null;
  const endCoords = end && nodes[end] ? [nodes[end].y, nodes[end].x] : null;

  return (
    <>
      {startCoords && (
        <Marker position={startCoords} icon={startIcon}>
          <Popup>Start</Popup>
        </Marker>
      )}
      {endCoords && (
        <Marker position={endCoords} icon={endIcon}>
          <Popup>End</Popup>
        </Marker>
      )}
    </>
  );
}
