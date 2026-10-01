
import pandas as pd

RAW_FILE = "pharmeasy_orders_raw.csv"
OUTPUT_FILE = "orders_clean.csv"


def validate_schema(df, required_columns):
    missing_columns = [c for c in required_columns if c not in df.columns]

    if missing_columns:
        return False, {
            "status": "blocked_schema",
            "missing_columns": missing_columns
        }

    return True, {
        "status": "validated",
        "columns": list(df.columns)
    }


def clean_data():
    df = pd.read_csv(RAW_FILE)

    # Remove exact duplicates
    df = df.drop_duplicates().reset_index(drop=True)

    # Normalize region names
    df["region"] = df["region"].str.strip().str.title()

    # Fill missing categories using product-category mapping
    product_category_map = (
        df.dropna(subset=["category"])
          .drop_duplicates("product")
          .set_index("product")["category"]
    )

    df["category"] = df["category"].fillna(
        df["product"].map(product_category_map)
    )

    # Calculate category-level average profit margin
    df["profit_margin"] = df["profit_inr"] / df["sales_inr"]

    category_mean_margin = df.groupby("category")["profit_margin"].mean()

    # Fill missing profit values
    df["profit_inr"] = df["profit_inr"].fillna(
        (
            df["sales_inr"]
            * df["category"].map(category_mean_margin)
        ).round(2)
    )

    df = df.drop(columns=["profit_margin"])

    # Save cleaned data
    df.to_csv(OUTPUT_FILE, index=False)

    print("Cleaned rows:", len(df))
    print("Missing values:", df.isna().sum().sum())
    print("Duplicates:", df.duplicated().sum())


if __name__ == "__main__":
    clean_data()
