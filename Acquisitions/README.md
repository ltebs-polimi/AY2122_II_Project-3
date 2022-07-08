## Electronic Technologies and Biosensors Lab - Project 3
## Academic Year 2021/2022 - II Semester


# CLASSIFICATION ALGORITHM FOR GESTURE RECOGNITION

To train and build the classification algorithm able to discriminate the tennis shots by means of accelerometer and gyroscope data, we performed several acquisitions and compared different classifiers.


**ACQUISITION PROTOCOL**

Tennis movements acquired during each acquisition and related labels set: 

- FOREHAND : '0'
- BACKHAND : '1'
- SERVE : '2'
- NO-SHOT : '3'

The acquisitions have been made by following these settings:

* Duration of each acquisition 🡪 about 4 seconds
* Number of subjects trained 🡪 4
* Number of acquisitions for each tennis shot 🡪 10 for each subject
* Number of acquisitions ofr the 'no-shot' gesture 🡪 20 for 1 subject only
* Number of acquisition files 🡪 140 (present in the acquisitions_for_TRAINING folder)


**FEATURES ENGINEERING**

For each acquisition CSV file (400,7), we computed: 
- 1° quantile = 0.25
- 2° quantile (median)
- 3° quantile = 0.75
of every IMU measurement, thus summarizing each CSV acquisition file in a 19-dimensional array.

Having 140 acquisition CSV files, the resulting training set is a (140,19) dataframe, converted in the *training_dataset.csv* file.


**TRAINED CLASSIFIERS**

* Decision Tree
* Logistic Regression
* KNN
* Random Forest
* SVM

Among the reported classifiers, we chose Random Forest as it presented the best performances in terms of F1 score, overfitting and interpretability.


> Further details in *acquisition_protocol.pdf* file.