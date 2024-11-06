# Galaxy-Classification-Using-Discriminants
This project explores the efficiency of various discriminants, including Artificial Neural Networks (ANN), Boosted Decision Trees (BDT), Fisher, Mahalanobis, H-Matrix, and linear discriminants, in classifying stars and galaxies. The study applies different variable transformations (none, N, U, G, D, and PCA) to assess their impact on classification accuracy. ANN and BDT showed the highest efficiency, while Fisher, Mahalanobis, and linear discriminants achieved high accuracy using the U transformation, particularly in distinguishing between rounded and no-bulge galaxies. This project provides insights for improving cosmological classification accuracy through advanced discriminant techniques. 

# Acknowledgments
This project is based on original work by Iftach Sadeh from the ANNZ repository on GitHub. I modified the code and adapted the dataset for my own use case to analyze the classification of stars and galaxies. Special thanks to Iftach for his foundational work, which served as the basis for my modifications.

Original Repository: https://github.com/IftachSadeh/ANNZ

## Overview
This project focuses on improving the accuracy of galaxy and star classification by analyzing the performance of several discriminants, such as:

- Artificial Neural Networks (ANN)
- Boosted Decision Trees (BDT)
- Fisher
- Mahalanobis
- H-Matrix
- Linear Discriminants

Additionally, it explores the impact of different variable transformations (none, N, U, G, D, and PCA) on the efficiency of these discriminants. The analysis was carried out in two parts:

- Part A: Classifying stars and galaxies.
- Part B: Distinguishing between rounded galaxies and galaxies with no bulges.

## Key Findings
- ANN consistently outperformed all the evaluation parameters, including accuracy, precision, F1 score, and recall, across the discriminants, followed by BDT.
- Fisher, Mahalanobis, and linear discriminants showed strong performance with the U variable transformation, achieving an accuracy of 0.991 in Part A and 0.9306 in Part B.
- These findings highlight the potential of Fisher, Mahalanobis, and linear discriminants in cosmological classification, providing valuable insights for future research.

## Project Structure

- `thesis documents`
  - `santtosh_159193_fyp_final.pdf`: Thesis draft containing an in-depth analysis of the project, including methodology, experiments, results, and findings.
  - This thesis is available in: https://mega.nz/folder/eNsDDJbS#3-ydnHqzrpcH__CrfLcUvQ
    
- `scripts`: Folder containing the primary codebase.
  - `star_galaxy_classification.py`: script to run the classification using different discriminants (ANN, BDT, Fisher, Mahalanobis, H-Matrix, Linear Discriminants) and apply various transformations (none, N, U,                                        G, D, PCA) for the classification of part A ( star/galaxy classification)
  - `galaxy_classification.py`: script to run the classification of part B (no bulge/rounded galaxy classification) using the same discriminants from part A but applying only one most influencial transformation                                    from part A
  - `annz_rndCls_advanced.py`: additional script that provides additional configurations and explanations for the classification scripts above
    
- `data`: Contains the dataset used for classification
  - Part A: Refer to IftachSadeh github; examples/data/sgSeparation: download the data needed for star/galaxy seperation
  - Part B: Dataset for galaxy separation is a query process which was done in https://skyserver.sdss.org/casjobs/. The data, organized into tables, are displayed in the Schema Browser on the SDSS website 
            (https://skyserver.sdss.org/dr18/MoreTools/browser/). Samples were downloaded by  inputting the parameter name, followed by the table name. The following query was  written to obtain a sample of no 
            bulge galaxies for galaxy classification:
  
`SELECT
p.objID, p.psfMag_r, p.fiberMag_r, p.modelMag_r,
p.petroMag_r, p.petroRad_r, p.petroR50_r, p.petroR90_r, 
p.lnLStar_r, p.lnLExp_r, p.lnLDeV_r, p.mE1_r, p.mE2_r,
p.mRrCc_r, p.type_r, p.type, s.dr8objid, 
s.t01_smooth_or_features_a02_features_or_disk_flag, 
s.t02_edgeon_a04_yes_flag,s.t09_bulge_shape_a25_rounded_flag, s.t09_bulge_shape_a27_no_bulge_flag 
FROM PhotoPrimary AS p 
JOIN zoo2MainSpecz AS s ON p.objID = s.dr8objid 
WHERE 
s.t01_smooth_or_features_a02_features_or_disk_flag = 1 
AND s.t02_edgeon_a04_yes_flag = 1 
AND s.t09_bulge_shape_a27_no_bulge_flag = 1`

    This section (Part B) will experiment with three different types of datasets due to differences in the data for rounded and no bulge, where they contain 1170 and 360, respectively:
    - Dataset A: dataset (360:360) non-weighted
    - Dataset B: all data (1170:360) non-weighted
    - Dataset C: all data (1170:360) weighted
  
- `results`: Script for calculating evaluation metrics (accuracy, precision, recall, F1 score and confusion matrix) across different discriminants and transformations. Plots and charts generated to visualize the 
             performance of discriminants.
  - `thesis data SG.ipynb`: Evaluation script for Part A
  - `galaxy all data no wgt.ipynb`: Evaluation script for Part B (Dataset B)
  - `galaxy all data wgt.ipynb`: Evaluation script for Part B (Dataset C)
  - `galaxy equal data no wgt.ipynb`: Evaluation script for Part B (Dataset A)

## Conclusion
This project demonstrates the effectiveness of various discriminants in classifying stars and galaxies, as well as distinguishing between rounded galaxies and galaxies with no bulges. The study evaluated multiple discriminants, including Artificial Neural Networks (ANN), Boosted Decision Trees (BDT), Fisher, Mahalanobis, H-Matrix, and linear discriminants, across different variable transformations (none, N, U, G, D, and PCA).

In part A of the study, ANN consistently outperformed all other discriminants in terms of accuracy, precision, F1 score, and recall, making it the most reliable classifier overall. BDT also showed strong performance, closely following ANN. While Fisher, Mahalanobis, H-Matrix, and linear discriminants did not achieve the same level of overall efficiency, they demonstrated notable performance improvements when applying the U transformation, achieving the highest accuracy (0.991) in classifying stars and galaxies.

In part B, when distinguishing between rounded and no-bulge galaxies, Fisher, Mahalanobis, and linear discriminants again showed excellent classification performance with the U transformation, achieving an accuracy of 0.9306 and a precision of 0.9559. These discriminants proved particularly valuable when precision was prioritized, showing their ability to accurately classify galaxies while minimizing false positives.

In summary, while ANN is the most efficient classifier for the dataset, Fisher, Mahalanobis, H-Matrix, and linear discriminants provide valuable alternatives in specific settings, particularly with the use of variable transformations like U. These findings offer important insights for future research in astronomical classification, where the choice of discriminant and transformation can be tailored to the specific goals and characteristics of the dataset.



