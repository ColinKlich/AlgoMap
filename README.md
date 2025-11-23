# AlgoMap

AlgoMap is a web application that visualizes and compares the performance of different pathfinding algorithms on real-world map data.

## Features

*   **Algorithm Visualization:** Watch pathfinding algorithms like Breadth-First Search (BFS), Dijkstra's, and A* explore the map in real-time.
*   **Performance Comparison:** See a side-by-side comparison of algorithm execution time, path length, and number of nodes visited.
*   **Real-World Data:** Utilizes map data from OpenStreetMap, fetched using OSMnx.
*   **OSRM Integration:** Compares graph-based algorithms with the OSRM routing engine.
*   **Interactive Map:** Select start and end points directly on the map.

## Tech Stack

*   **Backend:** Python, FastAPI, NetworkX, OSMnx, Geopy
*   **Frontend:** React, Leaflet.js, Vite

## Quick Start

This project includes a `run.sh` script that automates the setup and execution of both the frontend and backend.

1.  **Make the script executable:**
    ```bash
    chmod +x run.sh
    ```

2.  **Run the script:**
    ```bash
    ./run.sh
    ```

The script will check for dependencies, install them if necessary, and start both the backend and frontend servers. The application will be available at `http://localhost:5173`.

## Manual Setup

### Prerequisites

*   Python 3.7+
*   Node.js 14+

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload --port 8000
    ```

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```

The application will be available at `http://localhost:5173`.

## Usage

1.  Open the application in your browser.
2.  Search for a location or pan and zoom to the desired area.
3.  Click on the map to set a start and end point for the pathfinding.
4.  The application will run the different algorithms and display the results, including the path on the map and performance metrics.
