import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# 讀取與 Lab7.py 相同資料夾中的 CSV
from pathlib import Path
csv_path = Path(__file__).resolve().parent / 'Bank_Customer.csv'
data = pd.read_csv(csv_path)

# 1. 去除無意義特徵
features = data.drop(columns=['customer_id', 'churn'])
y = data['churn']

# 2. 類別型資料轉換成數值型 (One-Hot Encoding)
features = pd.get_dummies(features, columns=['country', 'gender'], dtype=int)

# 3. 切割資料：80% Training / 20% Testing
X_train, X_test, y_train, y_test = train_test_split(
    features, y, test_size=0.2, random_state=42, stratify=y
)

# 4. 標準化連續數值特徵；僅使用訓練資料 fit，避免資料洩漏
numeric_columns = ['credit_score', 'age', 'tenure', 'balance',
                   'products_number', 'estimated_salary']
scaler = StandardScaler()
X_train = X_train.copy()
X_test = X_test.copy()
X_train[numeric_columns] = scaler.fit_transform(X_train[numeric_columns])
X_test[numeric_columns] = scaler.transform(X_test[numeric_columns])

# 5. 儲存前處理資料：合併已轉換的訓練與測試資料並還原原始列順序
pre_data = pd.concat([X_train, X_test]).sort_index()
pre_data['churn'] = y
output_path = Path(__file__).resolve().parent / 'Bank_Customer_Preprocessed.csv'
pre_data.to_csv(output_path, index=False)

# 6. 建立並訓練 Logistic Regression
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
pred = clf.predict(X_test)

print('訓練資料筆數：', len(X_train))
print('測試資料筆數：', len(X_test))
print('前處理後特徵數：', X_train.shape[1])
print('預測準確率：', str(accuracy_score(y_test, pred) * 100) + '%')
print('已儲存：', output_path)
