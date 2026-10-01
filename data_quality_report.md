
# Data Quality Report

## Accuracy

The cleaned dataset uses the provided deterministic source data and applies the required cleaning rules without changing valid source values unnecessarily.

## Completeness

Missing category values were filled using the product-to-category mapping, and missing profit values were filled using the category-level mean profit margin.

## Consistency

Region names were normalized using trimming and title case so that equivalent region values use one canonical format.

## Timeliness

The dataset covers April, May, and June 2026 and is suitable for the required monthly regional analysis.

## Validity

The cleaned dataset retains the required columns and valid data types for order date, quantity, sales, and profit fields.

## Uniqueness

Exact duplicate rows were removed during cleaning. The final dataset contains 0 duplicate rows.

## Relevance

The cleaned dataset contains the order, region, category, product, quantity, sales, and profit fields required for the PharmEasy Regional Pulse analysis.
