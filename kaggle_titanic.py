# -*- coding: utf-8 -*-
"""Kaggle_Titanic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1n1DNKYUDzy9x0yHCcf0yc3L1e3ra3uYw
"""

from google.colab import files
files.upload()

# Copying kaggle.json to .kaggle directory
!mkdir ~/.kaggle
!cp /content/kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# Downloading Titanic Dataset from Kaggle
!kaggle competitions download -c titanic

import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Reading test.csv and train.csv
raw_train = pd.read_csv('train.csv')
raw_test = pd.read_csv('test.csv')

# Printing the first 5 rows of the data
raw_train.head()

# Description of Training Data
raw_train.info()

# Dropping Cabin, Name and Ticket columns from training and test sets
raw_train = raw_train.drop('Cabin', axis=1)
raw_train = raw_train.drop('Name', axis=1)
raw_train = raw_train.drop('Ticket', axis=1)
raw_test = raw_test.drop('Cabin', axis=1)
raw_test = raw_test.drop('Name', axis=1)
raw_test = raw_test.drop('Ticket', axis=1)

# One Hot Encoding Sex, Embarked and PClass in both training and test sets
raw_train = pd.get_dummies(raw_train, columns=["Sex", "Embarked", "Pclass"])
raw_test = pd.get_dummies(raw_test, columns=["Sex", "Embarked", "Pclass"])

# Normalising Age, SibSp, Fare and Parch in both Training and Test Data
raw_train["Age"] = raw_train["Age"]/raw_train["Age"].max()
raw_train["SibSp"] = raw_train["SibSp"]/raw_train["SibSp"].max()
raw_train["Fare"] = raw_train["Fare"]/raw_train["Fare"].max()
raw_train["Parch"] = raw_train["Parch"]/raw_train["Parch"].max()
raw_test["Age"] = raw_test["Age"]/raw_test["Age"].max()
raw_test["SibSp"] = raw_test["SibSp"]/raw_test["SibSp"].max()
raw_test["Fare"] = raw_test["Fare"]/raw_test["Fare"].max()
raw_test["Parch"] = raw_test["Parch"]/raw_test["Parch"].max()

# Checking the total missing values in training data
raw_train.isnull().sum()

# There is a lot of missing values in Age
# We will replace it with the mean age
raw_train['Age'] = raw_train['Age'].fillna(raw_train['Age'].mean())

# Dropping the Passenger ID Column as it is not needed in training
raw_train = raw_train.drop('PassengerId', axis=1)

# Making X_train and y_train
X_train = raw_train.drop("Survived", axis=1)
y_train = raw_train["Survived"]

# MODEL
# 1. Create the model
model = tf.keras.Sequential([
tf.keras.layers.Dense(12, activation="relu"),
tf.keras.layers.Dense(8, activation="relu"),
tf.keras.layers.Dense(4, activation="relu"),
tf.keras.layers.Dense(1, activation="sigmoid")
])
# 2. Compile the Model
model.compile(loss=tf.keras.losses.BinaryCrossentropy(), optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
metrics=["accuracy"])
# 3. Fit the Model
history = model.fit(X_train, y_train, epochs = 250)

# Plotting the Loss and Accuracy over 250 epochs
pd.DataFrame(history.history).plot(title="Loss and Accuracy")

# Drop the Passenger id and store it in a new variable
X_test = raw_test.drop("PassengerId", axis=1)
PassengerId = raw_test["PassengerId"]

# X_test still has some missing data
X_test.isnull().sum()

# Putting Mean of Age and Fare
X_test['Age'] = X_test['Age'].fillna(X_test['Age'].mean())
X_test['Fare'] = X_test['Fare'].fillna(X_test['Fare'].mean())

# We now have the predictions on the test data
# Let's create a gender_submission.csv as mentioned in the Kaggle Website
output_df = pd.DataFrame(data=PassengerId, columns=["PassengerId"])
output_df["Survived"] = y_train.astype(int)

print(output_df)

# Converting the data frame to csv for uploading to Kaggle
output_df.to_csv('gender_submission.csv',index=False)

# Submitting the csv file we created to Kaggle Competition
!kaggle competitions submit -c titanic -f /content/gender_submission.csv -m Submission_1