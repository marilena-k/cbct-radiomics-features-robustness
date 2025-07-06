#calculation of ICC - gaussian noise edition
import pandas as pd
import pingouin as pg

# Load the cleaned dataset
df = pd.read_csv("path_for_merged_features_ready_for_icc.csv")

# Metadata columns
meta_cols = ['Mouse', 'Timepoint', 'Noise_Level']
feature_cols = [col for col in df.columns if col not in meta_cols]

icc_results = []

# Loop over each feature
for feature in feature_cols:
    try:
        temp = df[['Mouse', 'Noise_Level', feature]].dropna()
        temp = temp.rename(columns={feature: 'Value'})
        
        icc = pg.intraclass_corr(data=temp,
                                 targets='Mouse',
                                 raters='Noise_Level',
                                 ratings='Value')
        
        icc_row = icc[icc['Type'] == 'ICC2']  # ICC(2,1)
        icc_value = icc_row['ICC'].values[0]
        icc_results.append({'Feature': feature, 'ICC': icc_value})
    except Exception as e:
        print(f"Error calculating ICC for {feature}: {e}")

# Save ICC results
icc_df = pd.DataFrame(icc_results)
icc_df.to_csv("path_for_icc_results_full_radiomics.csv", index=False)

print("ICC results saved.")


#calculation of ICC - mask perturbations
import pandas as pd
from pingouin import intraclass_corr
import os

# Load the dataset
file_path = "path_for_icc_results_radiomics_features_full_morph_2.csv"
df = pd.read_csv(file_path)

# Separate metadata
metadata_cols = ["Mouse", "Timepoint", "Mask_Type"]
feature_cols = [col for col in df.columns if col not in metadata_cols]

# Prepare data structure to store ICC results
icc_results = []

# Loop through features and compute ICC(2,1) for each
for feature in feature_cols:
    # Subset dataframe for current feature and relevant grouping variables
    temp_df = df[["Mouse", "Timepoint", "Mask_Type", feature]].dropna()
    temp_df = temp_df.rename(columns={feature: "Feature_Value"})

    # Add a combined ID for each subject (Mouse + Timepoint)
    temp_df["Subject_ID"] = temp_df["Mouse"].astype(str) + "_" + temp_df["Timepoint"].astype(str)

    # Compute ICC using pingouin
    try:
        icc = intraclass_corr(data=temp_df,
                              targets="Subject_ID",
                              raters="Mask_Type",
                              ratings="Feature_Value")
        icc_val = icc.loc[icc["Type"] == "ICC2", "ICC"].values[0]
        icc_results.append({"Feature": feature, "ICC2": icc_val})
    except Exception as e:
        icc_results.append({"Feature": feature, "ICC2": None})

# Convert to DataFrame
icc_df = pd.DataFrame(icc_results)

# Save to CSV
output_path = "path_for_icc_results_icc_results_morph_perturbations.csv"
icc_df.to_csv(output_path, index=False)

# Show summary
icc_df.head()
