# cbct-radiomics-features-robustness
This repository contains the full pipeline developed for the master’s thesis project “Understanding the Dynamics of Cachexia: Assessing the Robustness of Radiomics Features Derived from CBCT Scans of Mice.” The code systematically quantifies how radiomics features from cone-beam computed tomography (CBCT) images respond to two clinically relevant perturbations: simulated Gaussian noise (mimicking acquisition variability) and morphological mask perturbations (simulating segmentation inaccuracies).

The ultimate goal is to identify robust, reproducible features suitable for non-invasive monitoring of body composition changes in preclinical cancer cachexia models.
Repository Structure:

    adding_morphological_mask_perturbations.py
    Automates morphological operations (erosion, dilation, opening, closing) on segmentation masks of skeletal muscle regions. Generates perturbed masks to assess sensitivity to segmentation inaccuracies.

    extract_features_from_perturbed_masks.py
    Extracts radiomics features from the CBCT images using PyRadiomics, pairing each image with its original and perturbed masks. Outputs a comprehensive feature matrix for ICC analysis.

    calculation_of_ICC.py
    Calculates intraclass correlation coefficients (ICCs) separately for:

        Features extracted from images with increasing Gaussian noise.

        Features extracted from morphological mask perturbations.
        ICC(2,1) is used to quantify feature reproducibility across perturbations.

    breaking_point_analysis.py
    Implements a cumulative ICC approach to determine the breaking point: the lowest cumulative noise level at which each feature’s ICC drops below 0.8. Outputs a list of robust features (those with ICC ≥0.8 up to maximum tested noise level) and a summary of feature stability.

Methodology Overview

    Image Perturbation

        Noise: Gaussian noise is progressively added to CBCT scans to simulate increasing acquisition variability (σ=10–100 HU).

        Mask perturbations: Morphological operations generate alternative segmentation masks, simulating realistic inaccuracies during ROI delineation.

    Feature Extraction

        PyRadiomics extracts 1581 features across first-order statistics, texture matrices (GLCM, GLRLM, GLSZM, etc.), and wavelet/log-sigma filters.

        Extraction is repeated for each perturbation scenario.

    Robustness Quantification

        ICC(2,1) is computed across perturbation levels.

        Features maintaining ICC ≥0.8 are considered robust.

        Breaking points identify noise thresholds beyond which feature reliability deteriorates.

    Outputs

        radiomics_features_full_morph_2.csv: Feature matrix for mask perturbations.

        path_for_icc_results_full_radiomics.csv: ICC results for noise perturbations.

        path_for_icc_results_icc_results_morph_perturbations.csv: ICC results for mask perturbations.

        path_for_breaking_points_results_0107.csv: Breaking point analysis results.

        path_for_robust_features_list_no_bp_0107.csv: Final list of robust features.

Dependencies

    Python ≥ 3.7

    PyRadiomics

    SimpleITK

    numpy

    pandas

    pingouin

    scikit-image


License

This repository is provided for academic and research purposes only. If you use this pipeline in your work, please cite the associated master’s thesis and acknowledge the methodology.

Acknowledgements

Developed as part of the Master’s in Health and Digital Transformation at Maastricht University, in collaboration with Maastro Clinic. Supervision by Prof. Frank Verhaegen. The project contributes to advancing robust radiomics biomarkers for monitoring disease progression in preclinical models.
