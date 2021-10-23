import math
import random
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

# print("Введите название файла:")
# filename = str(input())

tab = pd.read_table("s1.txt", delim_whitespace=True, names=['X', 'Y'])
x1 = tab['X'].to_numpy()
y1 = tab['Y'].to_numpy()

plt.scatter(x1, y1)
plt.savefig('output/no_clasters.png')

print("Введите количество кластеров:")
k = int(input())

cnt = len(tab)  # всего строк
center = [0] * k
center_x = [0.0] * k
center_y = [0.0] * k

# показывает какая точка к какому кластер у принадлежит
cls = [0] * cnt

# находим первые центроиды случайным образом
kol = 0
for i in center:
    ind = center.index(i)
    random_index = int(random.randint(0, cnt-1))
    if random_index == 0: kol += 1
    if kol > 1:
        while (random_index in center) or (random_index == 0):
            random_index = int(random.randint(0, cnt-1))
        center[ind] = random_index
        center_x[ind] = tab['X'][random_index]
        center_y[ind] = tab['Y'][random_index]
    else:
        center[ind] = random_index
        center_x[ind] = tab['X'][random_index]
        center_y[ind] = tab['Y'][random_index]

print(center_x)
print(center_y)

# кол-во переходов между кластерами
k_p = 1

# кол-во точек в каждом кластере
cls_count = [0] * k

while k_p > 0:
    k_p = 0
    # ищем принадлежность к кластерам
    i = 0
    cls_count = [0] * k
    for p in cls:
        xi = tab['X'][i]  # коорд точки
        yi = tab['Y'][i]

        j = 0
        m = 999999999.0
        min_i = 0
        for pt in center:
            # расстояние от точки до центров кластера
            d = math.sqrt(math.pow(xi - center_x[j], 2) + math.pow(yi - center_y[j], 2))
            if d < m:
                m = d
                min_i = j
            j += 1
        # увеличиваем кол-во переходов если новое значение кластера не равно прошлому
        if cls[i] != min_i:
            k_p += 1
        cls[i] = min_i
        cls_count[min_i] += 1
        i += 1
    print(k_p)

    # ищем новые центроиды
    i = 0
    for p in center:
        kc = 0.0
        sumx = 0.0
        sumy = 0.0

        j = 0
        for pt in cls:
            if pt == i:
                kc += 1.0
                sumx += tab['X'][j]
                sumy += tab['Y'][j]
            j += 1

        center_x[i] = sumx / kc
        center_y[i] = sumy / kc
        i += 1

print(cls_count)
print(sum(cls_count))

plt.clf()
i = 0
for pt in center:
    xn = []
    yn = []
    j = 0
    for p in cls:
        if p == i:
            xn.append(tab['X'][j])
            yn.append(tab['Y'][j])
        j += 1

    plt.scatter(xn, yn)
    i += 1

plt.savefig('output/claster.png')
# plt.show()

# среднее расстояние от точек до центроида по каждому кластеру
avg_d = []
i = 0
for pt in center:
    s = 0.0
    j = 0
    for p in cls:
        if p == i:
            d = math.sqrt(math.pow(tab['X'][j] - center_x[i], 2) + math.pow(tab['Y'][j] - center_y[i], 2))
            s += d
        j += 1
    s /= cls_count[i]
    avg_d.append(s)
    i += 1

print(avg_d)

fig, ax = plt.subplots()
ox = np.arange(len(center))
ax.bar(ox, height=avg_d)
ax.set_title("Среднее отклонение от центроидов кластера")
fig.savefig('output/sr.png')