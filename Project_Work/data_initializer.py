import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


# Importing the excel file containing our data
data = pd.read_excel(r'C:\Users\vince\intelligenza_computazionale\Campania.xlsx',index_col=None, na_values=['NA'], usecols="A:F, N, O")
data

# defining our pathways inside our mall
x_path = np.ravel((pd.DataFrame(data, columns = ['x_path']).dropna()).to_numpy())
y_path = np.ravel((pd.DataFrame(data, columns = ['y_path']).dropna()).to_numpy())
left_x_raw, left_y_raw = x_path[0:15], y_path[0:15]
midleft_x_raw, midleft_y_raw = x_path[15:20], y_path[15:20]
upper_x_raw, upper_y_raw = x_path[20:36], y_path[20:36]
right_x_raw, right_y_raw = x_path[35:44], y_path[35:44]
lower_x_raw, lower_y_raw = x_path[43:60], y_path[43:60]
midright_x_raw, midright_y_raw = x_path[60:len(x_path)], y_path[60:len(x_path)]



upper = interpolate.interp1d(upper_x_raw, upper_y_raw, kind = 'linear')
right = interpolate.interp1d(right_x_raw, right_y_raw, kind = 'linear')
lower = interpolate.interp1d(lower_x_raw, lower_y_raw, kind = 'linear')
midright = interpolate.interp1d(midright_x_raw, midright_y_raw, kind = 'linear')
def left(x): return np.zeros(len(x))
def midleft(x): return np.ones(len(x))*21


width= .1
left_x, left_y = left(np.arange(min(left_y_raw), max(left_y_raw), width)) , np.arange(min(left_y_raw), max(left_y_raw), width)
midleft_x, midleft_y = midleft(np.arange(22.2, 54.599999999999966, width)) , np.arange(22.2, 54.599999999999966, width)
upper_x, upper_y = np.arange(min(upper_x_raw), max(upper_x_raw), width), upper(np.arange(min(upper_x_raw), max(upper_x_raw), width))
right_x, right_y = np.arange(min(right_x_raw), max(right_x_raw), width), right(np.arange(min(right_x_raw), max(right_x_raw), width))
lower_x, lower_y = np.arange(min(lower_x_raw), max(lower_x_raw), width), lower(np.arange(min(lower_x_raw), max(lower_x_raw), width))
midright_x, midright_y = np.arange(min(midright_x_raw), max(midright_x_raw), width), midright(np.arange(min(midright_x_raw), max(midright_x_raw), width))



#initializing our points

Type = (data['Type'].dropna()).tolist()
Detail = (data['Detail_tag'].dropna()).tolist()
Name = (data['Name'].dropna()).tolist()
x = np.ravel((pd.DataFrame(data, columns = ['x']).dropna()).to_numpy())
y = np.ravel((pd.DataFrame(data, columns = ['y']).dropna()).to_numpy())
z = np.ravel((pd.DataFrame(data, columns = ['z']).dropna()).to_numpy())

Shops_ground = []
Food_ground = []
Entertainment_ground = []
Elevators_ground = []
Shops_first = []
Food_first = []
Elevators_first = []
Entrances = []

for i in range(len(x)):
    obj = [Type[i], Detail[i], Name[i], x[i], y[i], z[i]]
    if z[i] == 0:
        if Type[i] == "Structure":
            if Detail[i] == "Elevator":
                Elevators_ground.append(obj)
            else:
                Entrances.append(obj)
        elif Type[i] == "Food":
            Food_ground.append(obj)
        elif Type[i] == "Shop":
            Shops_ground.append(obj)
        elif Type[i] == "Entertainment":
            Entertainment_ground.append(obj)
    elif z[i]==1:
        if Type[i] == "Structure":
            if Detail[i] == "Elevator":
                Elevators_first.append(obj)
        elif Type[i] == "Food":
            Food_first.append(obj)
        elif Type[i] == "Shop":
            Shops_first.append(obj)



# initializing the distance between each shop and the nearest pathway

def distance(category):
    proj = []
    dist = []
    index = []
    for i in range(len(category)):
        pos, D =[], []
        for j in range(len(upper_x)):
            x,y = upper_x[j], upper_y[j]
            d = np.sqrt((x-category[i][3])**2+(y-category[i][4])**2)
            D.append(d)
            pos.append((x,y))
        for j in range(len(left_x)):
            x,y = left_x[j], left_y[j]
            d = np.sqrt((x-category[i][3])**2+(y-category[i][4])**2)
            D.append(d)
            pos.append((x,y))
        for j in range(len(midleft_x)):
            x,y = midleft_x[j], midleft_y[j]
            d = np.sqrt((x-category[i][3])**2+(y-category[i][4])**2)
            D.append(d)
            pos.append((x,y))
        for j in range(len(right_x)):
            x,y = right_x[j], right_y[j]
            d = np.sqrt((x-category[i][3])**2+(y-category[i][4])**2)
            D.append(d)
            pos.append((x,y))
        for j in range(len(midright_x)):
            x,y = midright_x[j], midright_y[j]
            d = np.sqrt((x-category[i][3])**2+(y-category[i][4])**2)
            D.append(d)
            pos.append((x,y))
        for j in range(len(lower_x)):
            x,y = lower_x[j], lower_y[j]
            d = np.sqrt((x-category[i][3])**2+(y-category[i][4])**2)
            D.append(d)
            pos.append((x,y))
        #print(D)

        for j in range(len(D)):
            if D[j]==min(D):
                dist.append(D[j]*0.5)
                proj.append(pos[j])
                break
                #print(min(D))
                #print(category[i][3], category[i][4], pos[j])
                #print(np.sqrt((pos[j][0]-category[i][3])**2+(pos[j][1]-category[i][4])**2)-D[j])
                #print("truth", [pos[j][0],category[i][3]], [pos[j][1], category[i][4]])

          
      
    return proj, dist


a = distance(Shops_ground)
b = distance(Food_ground)
c = distance(Entertainment_ground)
d = distance(Entrances)

for i in range(len(Shops_ground)):
    Shops_ground[i].append(a[0][i][0])
    Shops_ground[i].append(a[0][i][1])
    Shops_ground[i].append(a[1][i])

for i in range(len(Food_ground)):
    Food_ground[i].append(b[0][i][0])
    Food_ground[i].append(b[0][i][1])
    Food_ground[i].append(b[1][i])

for i in range(len(Entertainment_ground)):
    Entertainment_ground[i].append(c[0][i][0])
    Entertainment_ground[i].append(c[0][i][1])
    Entertainment_ground[i].append(c[1][i])

for i in range(len(Entrances)):
    Entrances[i].append(d[0][i][0])
    Entrances[i].append(d[0][i][1])
    Entrances[i].append(d[1][i])

plt.figure(figsize=(16,12))
for i in range(len(Shops_ground)):
    plt.scatter(Shops_ground[i][3], Shops_ground[i][4], c="red")
    plt.annotate(Shops_ground[i][2], (Shops_ground[i][3], Shops_ground[i][4]), size=10)
    plt.plot([a[0][i][0], Shops_ground[i][3]], [a[0][i][1], Shops_ground[i][4]], alpha = 0.3, c="red")

for i in range(len(Food_ground)):
    plt.scatter(Food_ground[i][3], Food_ground[i][4], c="green")
    plt.annotate(Food_ground[i][2], (Food_ground[i][3], Food_ground[i][4]), size=10)
    plt.plot([b[0][i][0], Food_ground[i][3]], [b[0][i][1], Food_ground[i][4]], alpha = 0.3, c="green")

for i in range(len(Entertainment_ground)):
    plt.scatter(Entertainment_ground[i][3], Entertainment_ground[i][4], c="blue")
    plt.annotate(Entertainment_ground[i][2], (Entertainment_ground[i][3], Entertainment_ground[i][4]), size=10)
    plt.plot([c[0][i][0], Entertainment_ground[i][3]], [c[0][i][1], Entertainment_ground[i][4]], alpha = 0.3, c="blue")

for i in range(len(Entrances)):
    plt.scatter(Entrances[i][3], Entrances[i][4], c="black")
    plt.annotate(Entrances[i][2], (Entrances[i][3], Entrances[i][4]), size=10)
    plt.plot([d[0][i][0], Entrances[i][3]], [d[0][i][1], Entrances[i][4]], alpha = 0.3, c="black")

plt.plot(left_x, left_y)
plt.plot(midleft_x, midleft_y)
plt.plot(upper_x, upper_y)
plt.plot(right_x, right_y)
plt.plot(lower_x, lower_y)
plt.plot(midright_x, midright_y)


plt.grid()
plt.show()


