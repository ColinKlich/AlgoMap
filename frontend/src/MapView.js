import { MapContainer, TileLayer, Polyline } from "react-leaflet";
import L from "leaflet";
import MapEvents from "./MapEvents";
import Markers from "./Markers";
import MapViewUpdater from "./MapViewUpdater";

export default function MapView({ results, nodes, start, end, onMapClick, center, zoom, pathColors }) {
  return (
    <MapContainer center={center} zoom={zoom} style={{ height: "100vh" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      <MapViewUpdater center={center} zoom={zoom} />
      <MapEvents onMapClick={onMapClick} />

      <Markers start={start} end={end} nodes={nodes} />

      {Object.entries(results).map(([algo, result]) => {
        if (!result || !Array.isArray(result.path_geometry)) {
          return null;
        }
        const flippedPathGeometry = result.path_geometry.map(segment => segment.map(([x, y]) => [y, x]));
        return flippedPathGeometry.map((segment, i) => (
          <Polyline key={`${algo}-${i}`} positions={segment} color={pathColors[algo]} weight={5} />
        ));
      })}

    </MapContainer>
  );
}