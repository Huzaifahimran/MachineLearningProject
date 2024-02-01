from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

app = Flask(__name__)

# Read data from a CSV file
file_path = "BankCustomerChurnPrediction.csv"
customer_data = pd.read_csv(file_path)
# Drop the "customer_id" column
customer_data = customer_data.drop("customer_id", axis=1)
# Convert categorical variables to factors
customer_data = pd.get_dummies(customer_data, columns=['country', 'gender', 'credit_card', 'active_member'], drop_first=True)
customer_data['churn'] = pd.Categorical(customer_data['churn'])
# Define features (all columns except 'churn')
features = customer_data.columns[customer_data.columns != 'churn']
# Split the data into training and testing sets
train_data, test_data = train_test_split(customer_data, test_size=0.3, random_state=456)

# Initialize and train the Random Forest model
churn_model = RandomForestClassifier(random_state=789)
churn_model.fit(train_data[features], train_data['churn'])
# Make predictions on the test set
predictions = churn_model.predict(test_data[features])
# Evaluate model performance

conf_matrix = confusion_matrix(test_data['churn'], predictions)
accuracy = accuracy_score(test_data['churn'], predictions)

print("Confusion Matrix:\n", conf_matrix)
print("Classification Accuracy:", round(accuracy, 4))



def convert_to_python_types(obj):
    """
    Recursively converts pandas DataFrame elements of type int64 to Python int.
    """
    if isinstance(obj, pd.DataFrame):
        return obj.apply(convert_to_python_types)
    elif isinstance(obj, pd.Series):
        if obj.dtype == 'int64':
            return obj.astype(int)
    return obj

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the request form
    data = request.json
    print(data)

    # Convert the dictionary to a DataFrame with a single row
    new_customer_df = pd.DataFrame(data , index=[0])

    # Make predictions using the trained model
    new_prediction = churn_model.predict(new_customer_df[features])

    # Display the prediction
    print("New Customer Prediction:", new_prediction[0])

    # Return the prediction as JSON
    return str(new_prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
