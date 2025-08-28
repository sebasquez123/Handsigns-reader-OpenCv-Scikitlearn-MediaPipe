from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib



def separar_datos(df):

    y = df['label']
    X = df.drop(["label", "timestamp"], axis=1, errors='ignore')
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y)
    return X_train, X_test, y_train, y_test


def get_accuracy(mln,X_train, X_test, y_train, y_test):
    model = DecisionTreeClassifier(max_leaf_nodes=mln,random_state=42)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    return accuracy_score(y_test, prediction)


def graficar_resultados(errores):
    df = pd.DataFrame(errores, columns=['max_leaf_nodes', 'accuracy'])
    # df.to_excel('errores.xlsx', index=False,float_format="%.2f",sheet_name='Errores de modelo')
    print(df)
    x = df['max_leaf_nodes']
    y = df['accuracy']

    plt.plot(x,y)
    plt.xlabel('max_leaf_nodes')
    plt.ylabel('accuracy')
    plt.title('Decision Tree Classifier')
    plt.show()

def preentrenamiento(processedPath):
    df = pd.read_csv(processedPath)
    X_train, X_test, y_train, y_test = separar_datos(df) 
    errores = []
    for mln in range(5,100,2):
        error = get_accuracy(mln,X_train, X_test, y_train, y_test)
        errores.append([mln,error])
    graficar_resultados(errores)

def entrenamiento_final(mln, processedPath):
    df = pd.read_csv(processedPath)
    X_train, X_test, y_train, y_test = separar_datos(df) 
    model = DecisionTreeClassifier(max_leaf_nodes=int(mln), random_state=42)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)
    error = accuracy_score(y_test, prediction)
    joblib.dump(model, 'models/modelo_entrenado.pkl')
    print('Modelo entrenado con una precisión de:', error * 100 , '%')

