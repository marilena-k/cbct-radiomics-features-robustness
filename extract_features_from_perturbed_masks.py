import os
import pandas as pd
import SimpleITK as sitk
from radiomics import featureextractor


base_dir = "path_to_thee_file" 
label_value = 1 
selected_cases = [
    {"mouse": "M01", "timepoints": ["T01", "T02"]},
    {"mouse": "M02", "timepoints": ["T01", "T02","T03"]},
    {"mouse": "M03", "timepoints": ["T01", "T02","T03", "T04", "T05", "T06"]},
    {"mouse": "M04", "timepoints": ["T01", "T02","T03", "T04", "T05", "T06"]},
    {"mouse": "M05", "timepoints": ["T01", "T02","T03", "T04", "T05", "T06"]},
    {"mouse": "M06", "timepoints": ["T01", "T02","T03"]},
    {"mouse": "M07", "timepoints": ["T01", "T02","T03"]},
    {"mouse": "M08", "timepoints": ["T01", "T02","T03", "T04", "T05", "T06"]},
    {"mouse": "M09", "timepoints": ["T01", "T02","T03", "T04", "T05"]},
    {"mouse": "M19", "timepoints": ["T01", "T02","T03", "T04", "T05", "T06"]},
    {"mouse": "M20", "timepoints": ["T01", "T02","T03", "T04", "T05", "T06"]},
    {"mouse": "M21", "timepoints": ["T01", "T02","T03", "T04", "T05", "T06"]}
]
morph_types = ["eroded", "dilated", "opened", "closed"]

# Output folder
output_dir = "C://Users//marilena//Downloads//m02_t01//Exp_3.5"
os.makedirs(output_dir, exist_ok=True)

# feature extractor 
extractor = featureextractor.RadiomicsFeatureExtractor("path_to_params.yaml")



all_features = []

for case in selected_cases:
    mouse = case["mouse"]
    for tp in case["timepoints"]:
        tp_path = os.path.join(base_dir, mouse, tp)
        image_file = f"Exp0.0_{mouse}_{tp}.nii.gz"
        image_path = os.path.join(tp_path, image_file)

        for morph in morph_types:
            mask_file = os.path.join(tp_path, "morph_masks", f"mask_{morph}.nii.gz")

            if not os.path.exists(image_path) or not os.path.exists(mask_file):
                print(f"Skipping missing files for {mouse}/{tp} [{morph}]")
                continue

            try:
                result = extractor.execute(image_path, mask_file, label=label_value)
                features = {k: v for k, v in result.items() if not k.startswith("diagnostics")}
                features.update({
                    "Mouse": mouse,
                    "Timepoint": tp,
                    "Mask_Type": morph
                })
                all_features.append(features)
                print(f" Features extracted: {mouse}/{tp} [{morph}]")
            except Exception as e:
                print(f" Extraction failed for {mouse}/{tp} [{morph}]: {e}")

#saving to csv
df = pd.DataFrame(all_features)
df.to_csv(os.path.join(output_dir, "radiomics_features_full_morph_2.csv"), index=False)
print("All features saved.")



