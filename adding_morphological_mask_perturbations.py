import os
import SimpleITK as sitk
import numpy as np
from skimage.morphology import ball, erosion, dilation, opening, closing

#directories
base_dir = r"path" 
label_value = 10  
radius = 1  # ball size for operations

# Define mice and timepoints
selected_cases = [
    {"mouse": "M0x", "timepoints": ["T01", "T02"]},
    {"mouse": "M0y", "timepoints": ["T01", "T02","T03"]},
    {"mouse": "M0z", "timepoints": ["T01", "T02","T03", "T04", "T05", "T06"]},
    
]


#Processing 
def process_mask(mask_path, save_dir):
    mask_img = sitk.ReadImage(mask_path)
    mask_arr = sitk.GetArrayFromImage(mask_img)
    binary = (mask_arr == label_value).astype(np.uint8)
    selem = ball(radius) #structural element 

    perturbed = {
        "eroded": erosion(binary, selem),
        "dilated": dilation(binary, selem),
        "opened": opening(binary, selem),
        "closed": closing(binary, selem),
    }

    os.makedirs(save_dir, exist_ok=True)
    for name, arr in perturbed.items():
        out_img = sitk.GetImageFromArray(arr.astype(np.uint8))
        out_img.CopyInformation(mask_img)
        sitk.WriteImage(out_img, os.path.join(save_dir, f"mask_{name}.nii.gz"))

# Loop through selected mice
for case in selected_cases:
    mouse = case["mouse"]
    for tp in case["timepoints"]:
        tp_path = os.path.join(base_dir, mouse, tp)
        mask_filename = f"Exp0.0_{mouse}_{tp}_postprocessed.nii.gz"
        mask_path = os.path.join(tp_path, mask_filename)
        output_dir = os.path.join(tp_path, "morph_masks")

        if not os.path.exists(mask_path):
            print(f"Missing mask for {mouse}/{tp}")
            continue

        print(f"Processing {mouse}/{tp}")
        process_mask(mask_path, output_dir)
