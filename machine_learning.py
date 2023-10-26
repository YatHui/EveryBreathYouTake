import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, max_error, r2_score
import matplotlib.pyplot as plt

# linear regresseion på pm2.5 och en column för att dra fram en global-predicition!!!

#Load data
df = pd.read_csv('health_and_air_final_df.csv')

# Create X = place/time and y = pm2.5 and deaths and take out testdata
X = df.loc[1:10,['Year']]
y = df.loc[1:10,['Death from ambient particulate matter pollution','PM 2.5 Airpollution']]

X_train, X_test,y_train, y_test = train_test_split(X, y, test_size=0.2)
# Cluster data, first country and only columns with data
Xy = df.iloc[1:10, 3:14]

# # Create model and add training data
# lin_model = LinearRegression()
# lin_model.fit(X_train, y_train)
# # create a predictions 
# y_predict = lin_model.predict(X_test)

# # Create logistic model and predictions
# X_train = X_train.to_numpy()
# X_test = X_test.to_numpy()
# y_train = y_train.to_numpy()
# y_test = y_test.to_numpy()
# # X_train = X_train.array(-1,1)
# # X_test = X_test.array(-1,1)
# # y_train = y_train.array(-1,1)
# # y_test = y_test.array(-1,1)
# model = LogisticRegression()
# model.fit(X_train, y_train)
# y_predict = model.predict(X_test)

# # Calculate mean squared, lower is better
# mse = mean_squared_error(y_test, y_predict)
# mae = mean_absolute_error(y_test, y_predict) #change negative into a absolute number
# # Check error-metric, 1.0 is too good, less than 0.5 is too bad
# r2score = r2_score(y_test, y_predict)
# print('mean squared e =', mse,'\nmean absolute e =', mae, '\nR2 score = ',r2score )

# #show test
# plt.plot(X_test, y_test, marker='o', linestyle='None')
# plt.show()


# Find 3 clusters in data
kmeans = KMeans(n_clusters=3, n_init='auto')
kmeans.fit(Xy)
# save labes and centroids
labels = kmeans.labels_
centers = kmeans.cluster_centers_

plt.scatter(Xy.iloc[:, 3], Xy.iloc[:, 10], c=labels, cmap='Accent')
# plt.scatter(centers[:, 3], centers[:, 10], marker="x", color='red')
plt.title(df.loc[1,['Location']])
plt.xlabel(Xy.columns[3])
plt.ylabel(Xy.columns[10])
# plt.show()

# Test loop
each_country = df['Location'].unique()

for country in each_country:
    country_df = df[df['Location'] == country]
    Xy = country_df.iloc[0:11, 3:14]
    # Find 2 clusters in data
    kmeans = KMeans(n_clusters=2, n_init='auto')
    kmeans.fit(Xy) 
    print(f'{country} has a kmeans inertia of {kmeans.inertia_}')
   