# Urbanrise Product Analytics (Docker Setup)

A full internal analytics prototype to fetch product data from an API, store it in MongoDB, generate business insights, and predict product rating quality using ML – now fully containerized with Docker.

---

## 🗂 Project Structure

```
project_root/
│
├── app.py                  # Streamlit main app
├── requirements.txt        # Python dependencies
├── Dockerfile              # Dockerfile for Streamlit app
├── docker-compose.yml      # Docker Compose file to run app + MongoDB
├── src/
│   ├── db_manager.py       # MongoDB connection and data fetching
│   ├── ingestion.py        # API ingestion into MongoDB
│   └── ml_engine.py        # ML model for rating prediction
├── README.md
```

---

## 🔹 Prerequisites

1. **Docker** ≥ 24.x  
2. **Docker Compose** ≥ v2.x (plugin or standalone)  
3. Internet connection for API data fetch  

Check versions:

```bash
docker --version
docker compose version
```

---

## 🔹 Docker Setup

### 1️⃣ Build and Run Containers

In project root, run:

```bash
docker compose up --build
```

- Builds the Streamlit app image and starts MongoDB.  
- Streamlit app will be available at [http://localhost:8501](http://localhost:8501).  
- MongoDB is mapped to host port **27018** to avoid conflicts with local MongoDB.

### 2️⃣ Run in Detached Mode

```bash
docker compose up -d --build
```

- Runs containers in the background.

### 3️⃣ Stop Containers

```bash
docker compose down
```

- Stops and removes containers.  
- Add `-v` to also remove volumes (optional):

```bash
docker compose down -v
```

---

## 🔹 Docker Configuration Notes

### Dockerfile

- Uses `python:3.11-slim`  
- Installs dependencies from `requirements.txt`  
- Exposes port `8501` for Streamlit  
- Default command: `streamlit run app.py`  

### docker-compose.yml

- **Services**:
  - `mongo` → MongoDB database, host port 27018, container port 27017  
  - `app` → Streamlit app, depends on `mongo`  

---

## 🔹 Using the App

1. **Fetch Data from API** → Pull products from DummyJSON API and store in MongoDB.  
2. **Train Model** → Train ML model to predict high-rated products.  
3. **Business Insights Tab** → Explore charts for price, rating, stock risk, and discount strategy.  
4. **Prediction Tab** → Input `price`, `discount %`, `stock` to predict rating quality.

---

## 🔹 Troubleshooting

- **Check Docker Compose version**:

```bash
docker compose version
```

- **Check logs**:

```bash
docker compose logs -f
```

- **Port conflicts** → MongoDB host port is 27018, adjust if needed in `docker-compose.yml`.

---

## 🔹 License

MIT License – Free for internal prototyping and learning.
