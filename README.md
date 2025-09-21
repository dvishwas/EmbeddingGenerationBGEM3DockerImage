# BGE-M3 Docker Image

A Docker image for BGE-M3 embeddings generation optimized for vector databases and RunPod deployment with NVIDIA GPU support.

## Features

- BGE-M3 model for high-quality embeddings
- Flask API with batch processing support
- NVIDIA GPU acceleration (CUDA 11.8)
- Automatic GPU/CPU detection
- Optimized for vector database integration
- Health check endpoints
- Comprehensive logging
- RunPod compatible

## Requirements

- NVIDIA GPU with CUDA support (recommended)
- Docker with NVIDIA Container Runtime
- 8GB+ GPU memory recommended

## API Endpoints

### Health Check
```
GET /health
```
Returns service status and model loading state.

Response:
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### Single/Multiple Text Embeddings
```
POST /embed
Content-Type: application/json

{
  "texts": ["text to embed"] // string or array of strings
}
```

Response:
```json
{
  "embeddings": [[0.1, 0.2, ...]], // array of embedding vectors
  "dimension": 1024,               // embedding dimension
  "count": 1                       // number of embeddings
}
```

### Batch Processing
```
POST /embed/batch
Content-Type: application/json

{
  "texts": ["text1", "text2", ...],
  "batch_size": 32  // optional, default: 32
}
```

## Docker Usage

### Build Image
```bash
docker build --platform linux/amd64 -t bge-m3-api .
```

### Run Container (GPU)
```bash
docker run --gpus all -p 5000:5000 bge-m3-api
```

### Run Container (CPU fallback)
```bash
docker run -p 5000:5000 bge-m3-api
```

### Environment Variables
- `PORT`: API port (default: 5000)

## RunPod Deployment

1. Push to Docker Hub:
```bash
docker tag bge-m3-api your-username/bge-m3-api:latest
docker push your-username/bge-m3-api:latest
```

2. In RunPod:
   - Use custom container: `your-username/bge-m3-api:latest`
   - Expose port: 5000
   - Recommended GPU: RTX 4090 or A100
   - Memory: 16GB+ recommended
   - CUDA version: 11.8+

## Example Usage

```python
import requests

# Generate embeddings
response = requests.post('http://localhost:5000/embed', 
    json={'texts': ['Hello world', 'Vector database']})
embeddings = response.json()['embeddings']

# Batch processing
response = requests.post('http://localhost:5000/embed/batch',
    json={'texts': texts_list, 'batch_size': 16})
```

## Performance Notes

- Model loads on startup (~30-60 seconds on GPU)
- Embedding dimension: 1024
- Supports texts up to 8192 tokens
- Batch processing recommended for multiple texts
- Uses FP16 for memory efficiency
- GPU acceleration provides 5-10x speedup over CPU

## Logging

All requests and errors are logged with timestamps. Check container logs:
```bash
docker logs <container_id>
```
