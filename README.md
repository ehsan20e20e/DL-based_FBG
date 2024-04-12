# DL-based_FBG
Animation Abstract (loading ... please wait):

![DL-based_FBG3](https://github.com/ehsan20e20e/DL-based_FBG/assets/106914575/3c31a34b-d2a8-4d8d-b369-bcd94870857d)

## Describtion
The provided repository serves as a demonstration of the application of deep learning techniques in the prediction of the spectral response of all-optical plasmonic switches. This repository is based on the extensive research presented in the paper titled "Enabling_inverse_design_of_chirped_apodized_fiber_Bragg_grating_with_deep_learning." It has been designed to address inverse design challenges, with a specific focus on the fields of photonics and optics.
#### Instructions
The following guidelines provide detailed instructions for setting up and running a copy of the project on your local machine, thus enabling you to perform testing and development activities. These instructions are tailored to ensure accuracy and completeness when executing the project setup process. Consequently, we recommend that you adhere to them meticulously.
## Prerequisites
To obtain the results presented in this article, the use of the following software packages is recommended.
1) MATLAB (for optimization)
2) Python (for neural networks and deep learning)
3) Lumerical (for FDTD simulations)
4) COMSOL (for FEM simulations)
5) Qualitek-4 (for Taguchi method)
6) Minitab (for DOE)
   
Specifically, for this code, we utilized MATLAB version R2023a, Python version 3.7.13, and Spyder version 5.1.5 within Anaconda version 4.14.0, Ansys Lumerical version 2023 R1, COMSOL Multiphysics 6.1, Qualitek-4 version 14.2.0 and Minitab version 21.4.2. The project can be completed without these programs; however, the ability to compare speed and generate data will be limited without installing MATLAB and Python.
https://github.com/ehsan20e20e/SquareRR_AOPS/releases

## Geting_started
To utilize the contents of this repository, it is crucial to generate the necessary data for the all-optical switch structure using various FDTD (Finite-Difference Time-Domain) solvers such as Lumerical, RSoft, or MATLAB. These solvers enable the production and simulation of the optical switch structure, which facilitates the analysis of its performance and characteristics.

The file named "SquareRR_AOPS_Structure_file.fsp" is recommended for Lumerical simulations. To create the three-dimensional structure of AOPS, you can use the "Create SquareRR_AOPS_structure_FDTD_solver.lsf" file. For automatic data generation, the "SquareRR_AOPS_auto_FDTD_dataset_generator" script file is available. It is advisable to utilize these tools for efficient and accurate performance in your business or academic setting.

The proposed plasmonic switch structure's raw data is available in CSV files. These files have been provided to facilitate the reproduction of the graphs and results presented in this article.

===> Please be advised that there was an error in the input data related to the Drop port. The data was mistakenly entered as negative, which has been rectified in the written code. To ensure the accuracy of the data, we have applied the absolute value function to the input data. We apologize for any inconvenience this may have caused and assure you that we have taken the necessary measures to prevent such errors in the future.

### Forward_model
To train the forward model, utilizing the Python code provided in the 'SquareRR_AOPS_Forward_model.py' file is recommended. To this end, we have generated 147,456 unique examples through FDTD simulations and saved them in the "result_V.csv" file (Please take note of the following information: 18432 out of the total number of examples is sufficient.). As a prerequisite for executing the 'SquareRR_AOPS_Forward_model.py' file, it is essential to obtain the 'result_H.csv' file which constitutes a big data file with a size of 5.7 gigabytes. By following these steps, you can effectively train the forward model and achieve accurate results.

The 'result_V.csv' file can be accessed as a single file through the following link: 
https://github.com/ehsan20e20e/SquareRR_AOPS/releases/download/untagged-54db6d6bee08573b3623/result_V.rar

## Inverse_model
To facilitate the training of the inverse model, we recommend utilizing the Python source code provided in the 'SquareRR_AOPS_Inverse_model.py' file. We have meticulously curated 147,456 distinct examples derived from FDTD simulations and have saved them in the "result_H.csv" file, which can be accessed through the following links:
https://github.com/ehsan20e20e/SquareRR_AOPS/releases/download/untagged-54db6d6bee08573b3623/result_H.rar

The aforementioned instances may be employed to train the inverse model, while the provided Python code can be utilized to simplify the process. By capitalizing on these resources, you can significantly improve the efficiency and precision of your model training.

To execute the 'SquareRR_AOPS_Inverse_model.py' file, you need the 'result_H.csv' file. This file contains a significant amount of data, with a size of 1.6 gigabytes. Please ensure you have this file available before executing the aforementioned file.
