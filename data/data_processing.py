import pandas as pd
from sklearn.preprocessing import StandardScaler, PolynomialFeatures

def load_data(file_path):
    """Load dataset from a CSV file."""
    return pd.read_csv(file_path)

def scale_features(df):
    """Scale numerical features using StandardScaler."""
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    return df

def create_polynomial_features(df, degree=2):
    """Create polynomial features."""
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    poly_features = poly.fit_transform(df[numerical_cols])
    poly_feature_names = poly.get_feature_names_out(numerical_cols)
    poly_df = pd.DataFrame(poly_features, columns=poly_feature_names)
    df = df.join(poly_df)
    return df

def process_data(file_path):
    """Load, process, and return the dataset."""
    df = load_data(file_path)
    df = scale_features(df)
    df = create_polynomial_features(df)
    return df

if __name__ == "__main__":
    file_path = 'path_to_your_data.csv'  # Replace with your actual file path
    processed_data = process_data(file_path)
    processed_data.to_csv('processed_data_with_features.csv', index=False)
