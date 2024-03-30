import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def preprocess_data(input_file, output_file):
    # Load the dataset
    df = pd.read_csv(input_file)

    # Perform preprocessing steps
    # For example:
    # - Handling missing values
    # - Encoding categorical variables
    # - Feature scaling or normalization
    # - Splitting the dataset into training and testing sets

    # Handle missing values (replace NaN values with mean)
    df.fillna(df.mean(), inplace=True)

    # Encode categorical variables (if any)
    # Example:
    # df = pd.get_dummies(df, columns=['categorical_column'])

    # Split the dataset into features (X) and target variable (y)
    X = df.drop(columns=['target_column'])  # Adjust 'target_column' to your target variable
    y = df['target_column']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Perform feature scaling or normalization (if necessary)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save the preprocessed data to the output file
    processed_df = pd.concat([pd.DataFrame(X_train_scaled), pd.DataFrame(X_test_scaled), pd.DataFrame(y_train), pd.DataFrame(y_test)], axis=1)
    processed_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = "P2M_ML/Crop_recommendation.csv"
    output_file = "data/processed/Crop_recommendation_processed.csv"
    preprocess_data(input_file, output_file)
