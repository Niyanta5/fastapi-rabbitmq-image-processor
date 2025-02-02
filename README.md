# FastAPI + RabbitMQ Image Processing System

A distributed image processing system using FastAPI, RabbitMQ, and Docker. Upload images via an API endpoint, process them asynchronously via a worker, and store results.

## 📋 Features
- **Image Upload**: REST API endpoint for image uploads.
- **Message Queuing**: RabbitMQ decouples backend and worker.
- **Async Processing**: Worker processes images in the background.
- **Dockerized**: Easy setup with Docker Compose.

## 🛠️ Prerequisites
- Docker & Docker Compose
- Python 3.10

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fastapirabbitmqimageprocessing.git
cd fastapirabbitmqimageprocessing
```

### 2. Create Required Directories
```bash
mkdir -p uploaded_images processed_images
chmod -R a+rw uploaded_images processed_images
```

### 3. Start Services
```bash
docker-compose up --build
```

4. Access Services
FastAPI Backend: http://localhost:8000

RabbitMQ Dashboard: http://localhost:15672 (guest/guest)


### 📡 API Endpoints
###Upload Image
##POST /upload
```bash
curl -X POST -F "file=@/path/to/image.png" http://localhost:8000/upload
```
Check Processing Status (Example)
GET /status/{image_id}
```bash
{
  "status": "processed",
  "processed_image_url": "http://localhost:8000/processed_images/unique-id.png"
}
```






