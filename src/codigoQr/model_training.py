from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import pandas as pd
import joblib


# def separar_datos(df):
#     y= df.iloc[:,0:4]
#     x = df.iloc[:,4:]
#     X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.05)
#     return X_train, X_test, y_train, y_test


def separar_datos(df):
    y_train = df[['coor_X','coor_Y','rotacion']]
    x_train = df.iloc[:,4:]
    return x_train, y_train


def get_mean_absolute_error(mln,x_train, y_train):
    model = DecisionTreeRegressor(max_leaf_nodes=mln,random_state=1)
    model.fit(x_train, y_train)
    prediction = model.predict(x_train)
    return mean_absolute_error(y_train, prediction)
    

def graficar_resultados(errores):
    df = pd.DataFrame(errores, columns=['max_leaf_nodes', 'mean_absolute_error'])
    df.to_excel('errores.xlsx', index=False,float_format="%.2f",sheet_name='Errores de modelo')
    print(df)
    x = df['max_leaf_nodes']
    y = df['mean_absolute_error']
     
    plt.plot(x,y)
    plt.xlabel('max_leaf_nodes')
    plt.ylabel('mean_absolute_error')
    plt.title('Decision Tree Regressor')
     
     
def preentrenamiento(df):
    x_train, y_train = separar_datos(df) 
    errores = []
    for mln in range(5,100,5):
        error = get_mean_absolute_error(mln,x_train, y_train)
        errores.append([mln,error])
    graficar_resultados(errores)
    
def entrenamiento_final(mln,df):
    x_train, y_train = separar_datos(df) 
    print(x_train)
    model = DecisionTreeRegressor(max_leaf_nodes=mln,random_state=1)
    model.fit(x_train, y_train)
    prediction = model.predict(x_train)
    error = mean_absolute_error(y_train, prediction)
    joblib.dump(model, 'models/modelo_entrenado.pkl')
    print('Modelo entrenado con un error de:', error)


    
    
    
    
    
    