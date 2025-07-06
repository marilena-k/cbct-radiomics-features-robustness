import pandas as pd
import pingouin as pg


# Settings


# File paths 
features_path = "path_for_merged_features_ready_for_icc.csv"
output_bp_path = "path_for_breaking_points_results_0107.csv"
output_robust_path = "path_for_robust_features_list_no_bp_0107.csv"

# Cumulative noise levels matching the experiments
cumulative_levels = [10, 20, 30, 50, 60, 70, 80, 90, 100]

# ICC threshold for robustness
icc_threshold = 0.8


# Load data
print("Loading data...")
df = pd.read_csv(features_path)

# Identify feature columns
id_vars = ['Mouse', 'Timepoint', 'Noise_Level']
feature_cols = [col for col in df.columns if col not in id_vars]


# Compute breaking point
print("Computing cumulative ICCs and breaking points...")
breaking_points = {}

for feature in feature_cols:
    feature_breaking_point = None
    
    for cum_level in cumulative_levels:
        # Select rows up to current cumulative noise level
        subset = df[df['Noise_Level'].between(0, cum_level)].copy()
        subset['Subject'] = subset['Mouse'].astype(str) + '_' + subset['Timepoint'].astype(str)
        
        icc_df = subset[['Subject', 'Noise_Level', feature]].dropna()
        
        # Skip if not enough noise levels available
        if icc_df['Noise_Level'].nunique() < 2:
            continue
        
        # Calculate ICC2 (absolute agreement)
        icc_res = pg.intraclass_corr(
            data=icc_df,
            targets='Subject',
            raters='Noise_Level',
            ratings=feature
        )
        icc_value = icc_res.loc[icc_res['Type'] == 'ICC2', 'ICC'].values[0]
        
        print(f"Feature {feature}, cumulative up to noise {cum_level}%: ICC={icc_value:.3f}")
        
        if icc_value < icc_threshold:
            feature_breaking_point = cum_level
            break  # first cumulative noise level where ICC drops below threshold
    
    # If no breaking point found, mark as ">100" = robust up to max noise
    breaking_points[feature] = feature_breaking_point if feature_breaking_point is not None else ">100"

# Save breaking points

bp_df = pd.DataFrame(list(breaking_points.items()), columns=['Feature', 'Breaking_Point'])
bp_df.to_csv(output_bp_path, index=False)
print(f"\nBreaking points saved to: {output_bp_path}")


# Identify robust features

# Features with breaking point beyond max noise are robust
robust_features = [f for f, bp in breaking_points.items() if bp == ">100"]

# Save robust features
robust_df = pd.DataFrame(robust_features, columns=['Robust_Feature'])
robust_df.to_csv(output_robust_path, index=False)
print(f"Robust features saved to: {output_robust_path}")

# Print summary


print("Summary")
print("Total Features:", len(feature_cols))
print("Non-Robust Features:", len(feature_cols) - len(robust_features))
print("Robust Features:", len(robust_features))
print("\nSample robust features:")
print(robust_df.head(10))
