import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('digit-recognizer/train.csv')

# dataPreview = data.head()
# print(dataPreview)

data = np.array(data) #extract data into numpy arrays

m, n = data.shape #; print(m, n)
np.random.shuffle(data)

test = data[0:1000].T
y_test = test[0]
x_test = test[1:n]
x_test = x_test / 255 # normalize

train = data[1000: m].T
y_train = train[0]
x_train = train[1: n]
x_test = x_test / 255 

_, m_train = x_train.shape

#print(x_train[:, 0].shape)
#print(y_train)

def init_params():

    w_1 = np.random.randn(10, 784) * 0.01 #creates random weights between 0-1 for a 10 x 784 array
    b_1 = np.zeros((10 , 1)) # 

    w_2 = np.random.randn(10, 10) * 0.01 #creates random weights between 0-1 for a 10 x 784 array
    b_2 = np.zeros((10 , 1)) # 

    return [w_1, b_1, w_2, b_2]

def ReLU(z):
    return np.maximum(z, 0)

def softmax(z):

    exp = np.exp(z - np.max(z))

    return exp / exp.sum(axis = 0)

def forward_pass(w1, b1, w2, b2, x):
    z_1 = w1.dot(x) + b1
    a1 = ReLU(z_1)
    #print(w2.shape, a1.T.shape); exit()
    z_2 = w2.dot(a1) + b2

    a2 = softmax(z_2)

    return z_1, a1, z_2, a2

def one_hot(y):
    one_hot_y = np.zeros((y.size, y.max() + 1))
    one_hot_y[np.arange(y.size), y] = 1

    return one_hot_y.T

def deriv_ReLU(z): 
    return z > 0

def backward_prop(z_1, a1, z_2, a2, w2, x, y):
    m = y.size
    one_hot_y = one_hot(y)

    dZ2 = a2 - one_hot_y
    dW2 = 1 / m * dZ2.dot(a1.T)
    db2 = 1 / m * np.sum(dZ2)

    dZ1 = w2.T.dot(dZ2) * deriv_ReLU(z_1)
    dW1 = 1 / m * dZ1.dot(x.T)
    db1 = 1 / m * np.sum(dZ1)

    return dW1, db1, dW2, db2

def update_params(w1, b1, w2, b2, dW1, db1, dW2, db2, alpha):
    w1 = w1 - alpha * dW1
    b1 = b1 - alpha * db1

    w2 = w2 - alpha * dW2
    b2 = b2 - alpha * db2

    return w1, b1, w2, b2

def get_predictions(a2):
    return np.argmax(a2, 0)

def get_accuracy(predictions, y):
    #print(predictions, y)
    return np.sum(predictions == y) / y.size

def gradient_descent(x, y, epochs, alpha):
    w1, b1, w2, b2 = init_params()

    for epoch in range(epochs):
        z1, a1, z2, a2 = forward_pass(w1, b1, w2, b2, x)
        dw1, db1, dw2, db2 = backward_prop(z1, a1, z2, a2, w2, x, y)
        w1, b1, w2, b2 = update_params(w1, b1, w2, b2, dw1, db1, dw2, db2, alpha)

        if epoch % 50 == 0:
            print(f"Epoch: {epoch}")
            print(f"Accuracy: ", get_accuracy(get_predictions(a2), y))
    return w1, b1, w2, b2

def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_pass(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

def test_prediction(index, W1, b1, W2, b2):
    current_image = x_train[:, index, None]
    prediction = make_predictions(x_train[:, index, None], W1, b1, W2, b2)
    label = y_train[index]
    print("Prediction: ", prediction)
    print("Label: ", label)
    
    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')
    plt.show()

if __name__ == "__main__":

    w1, b1, w2, b2 = gradient_descent(x_train, y_train, 500, 0.001)

    test_pred = make_predictions(x_test, w1, b1, w2, b2)
    get_accuracy(test_pred, y_test)




