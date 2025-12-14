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




## 🔄 End-to-End Flow

### 1️⃣ API Ingestion

-   Product data is fetched from **DummyJSON API**
-   Data is stored in **MongoDB** for reuse and faster access

---

### 2️⃣ Data Processing

#### 📦 Business Category Mapping

Products are grouped into the following business categories using
rule-based mapping:

-   **Electronics**
-   **Home & Living**
-   **Fashion**
-   **Beauty**
-   **Daily Essentials**
-   **Others** (fallback for unmapped categories)

#### 💰 Price Segmentation

Products are segmented by price:

-   **Budget** → price ≤ 2000\
-   **Premium** → price \> 2000

---

### 3️⃣ Business Insights

The system generates insights such as:

-   ⭐ Rating distribution by **price segment**
-   🏷️ High-rated product contribution by **business category**
-   📊 Stock and discount-based performance insights

These insights help understand pricing strategy, inventory impact, and
customer preferences.

---

### 4️⃣ Machine Learning

#### 🎯 Problem Statement

Predict whether a product is **High Rated**.

-   **Target Variable**
    -   `High Rated = 1` if rating ≥ 4.0
    -   `Low Rated = 0` if rating \< 4.0

#### 🧩 Features Used

-   `price`
-   `discountPercentage`
-   `stock`

#### 🤖 Models Implemented

-   Logistic Regression
-   Random Forest Classifier
-   Gradient Boosting Classifier

#### 📐 Evaluation Metric

-   **Accuracy**

---

### 5️⃣ Prediction UI

A simple prediction interface allows users to:

1.  Input:
    -   Price
    -   Discount Percentage
    -   Stock Quantity
2.  Receive:
    -   Predicted Rating Class (**High / Low Rated**)
    -   Confidence score

---

## ⚖️ Assumptions & Trade-offs

-   Category mapping is **rule-based** with an `"Others"` fallback
-   Price threshold of **2000** is a business heuristic
-   Limited features result in **moderate model accuracy**
-   Prototype prioritizes **clarity and learning** over production
    scalability

---


## 🔹 License

MIT License – Free for internal prototyping and learning.
