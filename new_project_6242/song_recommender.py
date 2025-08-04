import pandas as pd
from surprise import Dataset, Reader
from surprise import SVD
from surprise.model_selection import GridSearchCV
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate
from surprise import accuracy
from collections import defaultdict
import pickle

df = pd.read_csv('data/User_Listening_History.csv', usecols=['user_id', 'track_id', 'playcount'])
# Cap values at the 99th percentile
cap_threshold = df['playcount'].quantile(0.99)  # Adjust based on your analysis
df['playcount'] = df['playcount'].clip(upper=cap_threshold)
reader = Reader(rating_scale=(1, df['playcount'].max()))  # Adjust the rating scale based on your data
# Load the dataset into Surprise format
data = Dataset.load_from_df(df[['user_id', 'track_id', 'playcount']], reader)

# Split the dataset into train and test set (e.g., 85% training, 15% testing)
trainset, testset = train_test_split(data, test_size=0.15)

#Run this for fine-tuning hyperparameters
#NOTE: THIS WILL TAKE A LONG TIME
param_grid = {
    'n_factors': [50, 100, 150],
    'n_epochs': [20, 30],
    'lr_all': [0.005, 0.01],
    'reg_all': [0.02, 0.1]
}
# Setup GridSearchCV
grid_search = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=5)

# Fit GridSearchCV
# Takes a long time to run
grid_search.fit(data)

# Best RMSE score
print(f"Best RMSE score: {grid_search.best_score['rmse']}")

# Parameters for the best RMSE score
print(f"Parameters for best RMSE score: {grid_search.best_params['rmse']}")

# Best MAE score
print(f"Best MAE score: {grid_search.best_score['mae']}")

# Parameters for the best MAE score
print(f"Parameters for best MAE score: {grid_search.best_params['mae']}")

best_params = grid_search.best_params['rmse']
algo = SVD(n_factors=best_params['n_factors'], n_epochs=best_params['n_epochs'], lr_all=best_params['lr_all'], reg_all=best_params['reg_all'])


algo = SVD()
# Train the model
algo.fit(trainset)

pickle.dump(algo, open('models/model_1.pkl','wb'))