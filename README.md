
# Urbanrise Product Analytics

A simple internal analytics prototype to fetch product data from an API, store it in MongoDB, generate business insights, and predict product rating quality using ML.

---

## 🗂 Project Structure

```
project_root/
│
├── app.py                 # Streamlit main app
├── requirements.txt       # Python dependencies
├── src/
│   ├── db_manager.py      # MongoDB connection and data fetching
│   ├── ingestion.py       # API ingestion into MongoDB
│   └── ml_engine.py       # ML model for rating prediction
```

---

## 🔹 Prerequisites

1. **Python** ≥ 3.10  
2. **MongoDB Community Edition** running locally at default port `27017`  
3. **Internet connection** for API data fetch  

---

## 🔹 Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd project_root
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Make sure MongoDB is running locally:

```bash
# Linux/macOS
sudo systemctl start mongod

# Windows
# Start MongoDB service from Services app or using MongoDB Compass
```

---

## 🔹 Usage

Start the Streamlit app:

```bash
streamlit run app.py
```

### Sidebar Controls:

- **Fetch Data from API** → Fetches products from DummyJSON and stores in MongoDB.
- **Train Model** → Trains a product rating ML model.

### Tabs:

- **Business Insights** → Interactive charts for product price, rating, stock risk, discount distribution, and category performance.
- **Prediction** → Input `price`, `discount`, and `stock` to predict if the product is high-rated (rating ≥ 4.0).

---

## 🔹 ML Model Notes

- Features: `price`, `discountPercentage`, `stock`  
- Target: `is_high_rated` → 1 if rating ≥ 4, else 0  
- Algorithms supported: `RandomForest`, `GradientBoosting`, `LogisticRegression`  
- Uses `StandardScaler` for preprocessing  

---

## 🔹 MongoDB Notes

- Database: `urbanrise_analytics`  
- Collection: `products`  
- Upsert is used: new products are inserted, existing ones are updated based on `id`.  

---

## 🔹 API Info

- API: [DummyJSON Products](https://dummyjson.com/products)  
- Fetches all products (`limit=0` for all)  

---

