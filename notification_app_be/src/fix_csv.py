import pandas as pd

for file in ["data/raw/train.csv", "data/raw/val.csv"]:
    # Load CSV, skipping bad lines
    df = pd.read_csv(file, on_bad_lines='skip', engine='python')
    
    # Keep only first two columns
    df = df.iloc[:, :2]
    
    # Rename columns to exactly what the model expects
    df.columns = ["code", "review"]
    
    # Drop fully empty rows
    df.dropna(how='all', inplace=True)
    
    # Save back
    df.to_csv(file, index=False)
    print(f"Fixed {file} -> columns: {df.columns.tolist()} rows: {len(df)}")

