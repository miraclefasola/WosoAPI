import pandas as pd

# The path to your raw CSV file
raw_csv_path = "WSL_2024_25_ALL_PLAYER_STATS_20250821_102053.csv"

# The path for your new, combined stats CSV
combined_csv_path = "WSL_2024_25_COMBINED_PLAYER_STATS.csv"

try:
    # Read the CSV file
    df = pd.read_csv(raw_csv_path)

    # Clean all column names by stripping whitespace
    df.columns = df.columns.str.strip()

    # Force the 'minutes' column to be numeric, replacing any errors with NaN
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")

    # Define columns that should be unique identifiers
    id_cols = ["player_id", "player_name", "position", "age"]

    # Identify all numeric columns for aggregation, excluding the ID columns
    numeric_cols_to_sum = list(
        set(df.select_dtypes(include=["number"]).columns.tolist()) - set(id_cols)
    )

    # --- Step 1: Aggregate the numeric columns ---
    # Fill any NaN values with 0 before summing to avoid errors
    combined_df = (
        df.groupby("player_id")[numeric_cols_to_sum].sum(min_count=1).reset_index()
    )

    # --- Step 2: Get the non-numeric data from the first entry of each player ---
    first_entries = df.drop_duplicates(subset=["player_id"])

    # Select only the ID columns
    non_numeric_df = first_entries[id_cols]

    # --- Step 3: Merge the aggregated and non-numeric dataframes ---
    final_df = combined_df.merge(non_numeric_df, on="player_id", how="left")

    # Reorder columns to a logical order
    final_cols = id_cols + numeric_cols_to_sum
    final_df = final_df[final_cols]

    # Save the new DataFrame to a CSV
    final_df.to_csv(combined_csv_path, index=False)

    print(f"Combined stats saved to: {combined_csv_path}")

except FileNotFoundError:
    print(f"Error: The file '{raw_csv_path}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
