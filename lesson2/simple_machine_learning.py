import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

titanic_content = pd.read_csv(open('train.csv'))
# print(titanic_content.head(10))
titanic_content = titanic_content.dropna()
age_fare = titanic_content[['Age', 'Fare']]
age_fare = age_fare[ (age_fare['Age'] > 22) & (age_fare['Fare'] < 400) & (age_fare['Fare'] > 130) ]
age = np.array(age_fare['Age'])
fare = np.array(age_fare['Fare'])

def loss(y_true, y_hats):
    return np.mean(np.abs(y_true - y_hats))

def model(x, a, b):
    return a * x + b

a = 1
b = 0

y_hats = np.array([model(x, a, b) for x in age])

eps = 20
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
learning_rate = 1e-2
min_loss = float('inf')
batch = 0

while True:
    if loss(y_true=fare, y_hats=y_hats) < eps:
        break

    # indices = np.random.choice(range(len(age)), size=10)

    # sample_x = age[indices]
    # sample_y = fare[indices]
    sample_x = age
    sample_y = fare

    new_a, new_b = a, b
    for d in directions:
        da, db = d
        if min_loss != float('inf'):
            _a = a + da * min_loss * learning_rate
            _b = b + db * min_loss * learning_rate
        else:
            _a, _b = a + db, b + db
    
        _y_hats = [model(x, _a, _b) for x in sample_x]
        l = loss(sample_y, _y_hats)

        if l < min_loss:
            min_loss = l
            new_a, new_b = _a, _b

    total = 10000

    if batch % 100 == 0:
        print('batch {}/ {} fare with {} * age + {}, with loss: {}'.format(batch, total, a, b, l))
    
    if batch > total: 
        break

    batch += 1

    a, b = new_a, new_b

plt.scatter(age, fare)
plt.plot(age, [model(x, a, b) for x in age])
plt.show()