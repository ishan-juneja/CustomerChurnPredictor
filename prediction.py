import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.dummy import DummyClassifier


data = pd.read_csv("Customer_Churn_Data.csv")

print(data.head())

data['Churn'] = data['Churn'].astype(int)

if 'customerID' in data.columns:
	data = data.drop('customerID', axis=1)

if 'StreamingTV' in data.columns:
	data = data.drop('StreamingTV', axis=1)

if 'PhoneService' in data.columns:
	data = data.drop('PhoneService', axis=1)

if 'multipleLines' in data.columns:
	data = data.drop('multipleLines', axis=1)


if 'StreamingMovies' in data.columns:
	data = data.drop('StreamingMovies', axis=1)

if 'DeviceProtection' in data.columns:
	data = data.drop('DeviceProtection', axis=1)


X = data.drop('Churn', axis=1) # all the data except the churn value
y = data['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}%".format(accuracy * 100))

y_pred_log = model.predict(X_test)


# Evaluation Metrics
def evaluate_model(y_true, y_pred, model_name):
	print(f"Model: {model_name}")
	print("Accuracy:", accuracy_score(y_true, y_pred))
	print("Precision:", precision_score(y_true, y_pred))
	print("Recall:", recall_score(y_true, y_pred))
	print("F1 Score:", f1_score(y_true, y_pred))
	print("ROC AUC:", roc_auc_score(y_true, y_pred))
	print("\nClassification Report:\n", classification_report(y_true, y_pred))

	# Confusion Matrix
	cm = confusion_matrix(y_true, y_pred)
	sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
	plt.title(f'Confusion Matrix for {model_name}')
	plt.xlabel('Predicted')
	plt.ylabel('Actual')
	plt.show()

sns.heatmap(data.corr(), cmap="coolwarm", annot=True)
plt.show()

# Evaluate Logistic Regression
evaluate_model(y_test, y_pred_log, "Logistic Regression")

dummy = DummyClassifier(strategy="most_frequent")
dummy.fit(X_train, y_train)
dummy_accuracy = dummy.score(X_test, y_test)
print(f"Baseline Accuracy: {dummy_accuracy:.2f}")




