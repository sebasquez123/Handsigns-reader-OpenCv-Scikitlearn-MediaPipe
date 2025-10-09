import time
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib

max_nodes = 200
step = 2
start = 5


def draw_progress (percentage,elapsed_time):
    '''Function to draw a progress bar in the console.'''
    
    bar_length = 40
    filled_length = int(bar_length * percentage // 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {percentage:.2f}%  -  Inference Time: {elapsed_time:.2f}s', end='\r')
    if percentage >= 99:
        print(f'\rProgress: |{'█' * 40}| 100% - Inference Time: {elapsed_time:.2f}s')

    return

def pre_training(processedPath):
    '''Function to train the model and find the best tree depth parameter.'''
    
    df = pd.read_csv(processedPath)
    X_train, X_test, y_train, y_test = split_data(df) 
    errores = []
    for mln in range(start,max_nodes,step):
        time_start = time.time()
        error = get_accuracy(mln,X_train, X_test, y_train, y_test)
        time_end = time.time()
        errores.append([mln,error])
        mln_percentage = ((mln - start) / (max_nodes - start)) * 100
        elapsed_time = time_end - time_start
        draw_progress(mln_percentage,elapsed_time)
    draw_results(errores)

def final_training(mln, processedPath):
    '''Function to train the final model with the best tree depth parameter.'''
    
    df = pd.read_csv(processedPath)
    X_train, X_test, y_train, y_test = split_data(df) 
    model = DecisionTreeClassifier(max_leaf_nodes=int(mln), random_state=42)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    error = accuracy_score(y_test, prediction)
    
    joblib.dump(model, 'models/trained_model.pkl')

    print('Model trained with accuracy:', error * 100 , '%')
    
    return

def split_data(df):
    '''Function to split the data into training and testing sets.'''
    
    y = df['label']
    X = df.drop(["label", "timestamp"], axis=1, errors='ignore')
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y)
    
    return X_train, X_test, y_train, y_test


def get_accuracy(mln,X_train, X_test, y_train, y_test):
    '''Function to test the model and get its accuracy with a determined max_leaf_nodes parameter.
    In this case, we use accuracy as the metric, because it is a multi-class classification problem,
    if it was a regression problem, we would use RMSE (Root Mean Squared Error) or MAE (Mean Absolute Error).'''
    
    model = DecisionTreeClassifier(max_leaf_nodes=mln,random_state=42)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    
    return accuracy_score(y_test, prediction)


def draw_results(errores):
    '''Function to plot the accuracy results with different max_leaf_nodes parameters.
    This helps to visualize the best parameter for the Decision Tree Classifier for human comprehension.'''
    
    df = pd.DataFrame(errores, columns=['max_leaf_nodes', 'accuracy'])
    print(df)
    x = df['max_leaf_nodes']
    y = df['accuracy']

    plt.plot(x,y)
    plt.xlabel('max_leaf_nodes')
    plt.ylabel('accuracy')
    plt.title('Decision Tree Classifier')
    plt.show()

