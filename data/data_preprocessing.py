import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

def load_data(file_path):
    """Load dataset from a CSV file."""
    return pd.read_csv(file_path)

def handle_missing_values(df):
    """Handle missing values in the dataset."""
    # Impute numerical columns with the median
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    imputer = SimpleImputer(strategy='median')
    df[numerical_cols] = imputer.fit_transform(df[numerical_cols])
    
    # Impute categorical columns with the most frequent value
    categorical_cols = df.select_dtypes(include=['object']).columns
    imputer = SimpleImputer(strategy='most_frequent')
    df[categorical_cols] = imputer.fit_transform(df[categorical_cols])
    
    return df

def encode_categorical_variables(df):
    """Encode categorical variables using Label Encoding."""
    categorical_cols = df.select_dtypes(include=['object']).columns
    label_encoder = LabelEncoder()
    for col in categorical_cols:
        df[col] = label_encoder.fit_transform(df[col])
    return df

def preprocess_data(file_path):
    """Load, preprocess, and return the dataset."""
    df = load_data(file_path)
    df = handle_missing_values(df)
    df = encode_categorical_variables(df)
    return df

if __name__ == "__main__":
    file_path = 'path_to_your_data.csv'  # Replace with your actual file path
    processed_data = preprocess_data(file_path)
    processed_data.to_csv('processed_data.csv', index=False)
