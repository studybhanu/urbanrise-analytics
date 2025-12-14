import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

class ProductRatingModel:
    def __init__(self):
        self.model = None
        self.algorithm = "RandomForest"  # default
        self.features = ['price', 'discountPercentage', 'stock']
        self.target = 'is_high_rated'
        self.accuracy = None

    def _preprocess(self, df):
        df = df.dropna(subset=self.features + ['rating'])
        df[self.target] = (df['rating'] >= 4.0).astype(int)
        X = df[self.features]
        y = df[self.target]
        return X, y

    def train(self, df, algorithm=None):
        if df.empty:
            return "Data is empty, cannot train."

        if algorithm:
            self.algorithm = algorithm

        X, y = self._preprocess(df)

        # Scale features for some algorithms
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )

        if self.algorithm == "LogisticRegression":
            self.model = LogisticRegression()
            self.model.fit(X_train, y_train)

        elif self.algorithm == "RandomForest":
            param_grid = {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 5],
                "min_samples_leaf": [1, 2]
            }
            base_model = RandomForestClassifier(random_state=42)
            grid = GridSearchCV(base_model, param_grid, cv=5, scoring="accuracy")
            grid.fit(X_train, y_train)
            self.model = grid.best_estimator_

        elif self.algorithm == "GradientBoosting":
            param_grid = {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.05, 0.1],
                "max_depth": [3, 5, 7]
            }
            base_model = GradientBoostingClassifier(random_state=42)
            grid = GridSearchCV(base_model, param_grid, cv=5, scoring="accuracy")
            grid.fit(X_train, y_train)
            self.model = grid.best_estimator_

        else:
            return f"Unknown algorithm: {self.algorithm}"

        # Evaluate
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        return f"Model trained using {self.algorithm}. Accuracy: {self.accuracy:.2f}"

    def predict(self, price, discount, stock):
        if not self.model:
            return None, None
        input_data = pd.DataFrame([[price, discount, stock]], columns=self.features)
        
        # Standardize input for Logistic Regression or Gradient Boosting
        if self.algorithm in ["LogisticRegression", "GradientBoosting"]:
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            input_data = scaler.fit_transform(input_data)

        prediction = self.model.predict(input_data)[0]
        if hasattr(self.model, "predict_proba"):
            probability = self.model.predict_proba(input_data)[0][1]  # Prob of High Rated
        else:
            probability = 1.0 if prediction == 1 else 0.0

        label = "High Rated (> 4.0)" if prediction == 1 else "Low Rated (< 4.0)"
        return label, probability
