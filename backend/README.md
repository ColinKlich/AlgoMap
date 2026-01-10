# AlgoMap Backend

AlgoMap Backend is a high-performance service designed to handle graph-based routing and pathfinding tasks. It provides implementations of popular algorithms such as A*, Dijkstra, and Greedy BFS, and is built using FastAPI for scalability and ease of use.

## Features
- **Routing Algorithms**: Supports A*, Dijkstra, Bidirectional Dijkstra, Greedy BFS, and more.
- **Graph Processing**: Utilizes `networkx` and `osmnx` for efficient graph operations.
- **RESTful API**: Built with FastAPI for high performance and easy integration.
- **Scalable**: Containerized for deployment in cloud environments and Kubernetes clusters.

## Getting Started

### Prerequisites
- Docker installed on your system
- Kubernetes cluster (optional, for deployment)

### Running the Backend with Docker

1. Pull the Docker image from Docker Hub:
   ```bash
   docker pull tsilver1/algomap-backend:v1.1
   ```

2. Run the container:
   ```bash
   docker run -p 8001:8001 tsilver1/algomap-backend:v1.1
   ```

3. Access the API at `http://localhost:8000`.

### API Endpoints
The backend exposes the following endpoints:
- `GET /route`: Calculate the shortest path between two points.
- `POST /upload-graph`: Upload a custom graph for routing.
- `GET /health`: Health check endpoint.

### Example Request
#### Calculate Route
```bash
curl -X GET "http://localhost:8000/route?start=lat1,lon1&end=lat2,lon2"
```

## Deployment

### Kubernetes Deployment
To deploy the backend on a Kubernetes cluster:

1. Create a deployment:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: algomap-backend
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: algomap-backend
     template:
       metadata:
         labels:
           app: algomap-backend
       spec:
         containers:
         - name: algomap-backend
           image: tsilver1/algomap-backend:v1.1
           ports:
           - containerPort: 8000
   ```

2. Expose the deployment as a service:
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: algomap-backend
   spec:
     selector:
       app: algomap-backend
     ports:
       - protocol: TCP
         port: 80
         targetPort: 8000
     type: ClusterIP
   ```

3. Set up an ingress resource:
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: algomap-backend-ingress
     annotations:
       nginx.ingress.kubernetes.io/rewrite-target: /
   spec:
     rules:
     - host: algomap.example.com
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: algomap-backend
               port:
                 number: 80
   ```

4. Apply the YAML files:
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl apply -f ingress.yaml
   ```

5. Point your domain (`algomap.example.com`) to the ingress controller's external IP.

## Docker Hub Repository
The Docker image for this backend is available on Docker Hub:
[https://hub.docker.com/r/tsilver1/algomap-backend](https://hub.docker.com/r/tsilver1/algomap-backend)

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License.