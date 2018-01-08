import pandas as pd
import numpy as np
import re
from timeit import default_timer as timer
from datetime import datetime

path = 'C:/Users/User/eurusd RawData.csv'
lines = [line for line in open(path)]
data = pd.read_csv(path, sep=',', header=None)

data.loc[:, '%Past'] = 0
data.loc[:, '%Future'] = 0
data.loc[:, 'Length'] = 0

data.columns.values[0] = 'Local Time'
data.columns.values[1] = 'Open'
data.columns.values[2] = 'High'
data.columns.values[3] = 'Low'
data.columns.values[4] = 'Close'
data.columns.values[5] = 'Volume'

for line in data.iloc[:, 0]:
    datetime.strptime(line, '%d.%m.%Y %H:%M:%S.%f')
for line in data.iloc[:, 1]:
    float(line)
for line in data.iloc[:, 2]:
    float(line)
for line in data.iloc[:, 3]:
    float(line)
for line in data.iloc[:, 4]:
    float(line)
for line in data.iloc[:, 5]:
    int(line)
for line in data.iloc[:, 6]:
    float(line)
for line in data.iloc[:, 7]:
    float(line)
for line in data.iloc[:, 8]:
    int(line)


Results = []
index = len(data)
x = 0
while x < index:
    x = x + 1
    Results.append(0)


def filler_p():
    global count
    Results[count] = 1


def filler_n():
    Results[count] = 2


data['Length'] = (data.iloc[:, 2].values - data.iloc[:, 3].values)

i = 0
index = len(data.iloc[:, 4]) - 2


results = []

while i <= index:
    i = i + 1
    current = data.iloc[i, 4]
    previous = data.iloc[i - 1, 4]
    result = (current - previous) / previous
    results.append(result)

results.insert(0, 0)
array = np.asarray(results)
data['%Past'] = array

z = -1
zIndex = len(data.iloc[:, 4]) - 3
results2 = []

while z <= zIndex:
    z = z + 1
    current2 = data.iloc[z, 4]
    future = data.iloc[z + 1, 4]
    result2 = (current2 - future) / future
    results2.append(result2)

results2.insert(len(data.iloc[:, 4]), 0)
arrayZ = np.asarray(results2)
data['%Future'] = arrayZ


"""Model Functions"""

y = 0
x = 0
z = 0


def extra():
    global x
    if z > x:
        k = z - x
        x = x + k
    else:
        x = z + x
    global Past
    Past = data.iloc[x, 6]
    global Future
    Future = data.iloc[x, 7]


def add():
    global y
    y = y + 1
    global z
    z = y + 1
    global close1
    global close2
    close1 = data.iloc[x+y, 4]
    close2 = data.iloc[x+z, 4]


def add_x():
    global close1
    global close2
    global y
    global z
    close1 = data.iloc[x + y, 4]
    close2 = data.iloc[x + z, 4]

    if close2 > close1:
        y = y + 1
        z = y + 1
        add_x()
    else:
        extra()


def add_y():
    global close1
    global close2
    global y
    global z
    close1 = data.iloc[x + y, 4]
    close2 = data.iloc[x + z, 4]

    if close2 < close1:
        y = y + 1
        z = y + 1
        add_y()
    else:
        extra()

start = timer()

"""Positive Model"""

Index = (len(data.iloc[:, 4]) - 3)

count = 0
while x <= Index:
    y = 0
    z = y + 1
    x = x + 1
    Past = data.iloc[x, 6]
    Future = data.iloc[x, 7]
    close1 = data.iloc[x+y, 4]
    close2 = data.iloc[x+z, 4]

    if Past < 0:
        count = x
        if Future > 0:
            if close2 > close1:
                add()
                while close2 > close1:
                    add_x()
                    if Past > 0:
                        if Future < 0:
                            filler_p()


"""Negative model"""

y = 0
x = 0
z = 0
count = 0

while x <= Index:
    y = 0
    z = y + 1
    x = x + 1
    Past = data.iloc[x, 6]
    Future = data.iloc[x, 7]
    close1 = data.iloc[x+y, 4]
    close2 = data.iloc[x+z, 4]

    if Past > 0:
        count = x
        if Future < 0:
            if close2 < close1:
                add()
                while close2 < close1:
                    add_y()
                    if Past < 0:
                        if Future > 0:
                            filler_n()
end = timer()
print(end - start, ' Model Time')

start = timer()

"""Statistic"""

change = []
x = 0

while x <= Index:
    x = x + 1
    if data.iloc[x, 6] >= 0:
        change.append(1)
    elif data.iloc[x, 6] < 0:
        change.append(2)

Percentage1 = (change.count(1)) / (len(change))
Percentage2 = (change.count(2)) / (len(change))

Percentage1 = round(Percentage1, 2)
Percentage2 = round(Percentage2, 2)

print(str(Percentage1) + '%' + ' Positive Change')
print(str(Percentage2) + '%' + ' Negative Change')

print(str(Results.count(1)) + ' Positive models')
print(str(Results.count(2)) + ' Negative models')

end = timer()
print(end - start, ' Statistic Time')
print(data)
a, b, c, d = path.split('/')

pattern = r'(.*)(.csv)'
match = re.match(pattern, d)
if match:
    j = match.group(1) + '_prepared' + match.group(2)

#data.to_csv(j, sep='\t', header=False, index=False)

