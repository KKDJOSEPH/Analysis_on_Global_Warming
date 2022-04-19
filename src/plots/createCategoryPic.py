
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import imageio


def load_dataset(filename):
    '''Loads an example of market basket transactions from a provided csv file.

    Returns: A list (database) of lists (transactions). Each element of a transaction is 
    an item.
    '''

    with open(filename,'r') as dest_f:
        data_iter = csv.reader(dest_f, delimiter = ',', quotechar = '"')
        data = [data for data in data_iter]
        data_array = np.asarray(data)
        
    return data_array

category = load_dataset("../../Data/CarbonBudget/Fossil_Emissions_by_Category.csv")
dataset = category[1:].astype(np.float)

result = pd.DataFrame(dataset, columns = category[0])
# result = result.set_index(result.iloc[:,0])
result = result.iloc[:, 1:]
df1 = pd.DataFrame(result,columns=['Coal','Oil','Gas','Cement.emission','Flaring', 'Other'])
for i in range(62):
    fig = df1.loc[i].sort_values().plot(kind='barh', figsize=(30,20), color=['darkred', 'gold', 'lime', 'purple', 'navy', 'lightcoral'], xticks=[1000, 2000, 3000, 4200], fontsize=20)
    plt.title('Year {}'.format(1959 + i), fontdict={'fontsize':40})
    plt.savefig('/tmp/page_{}.png'.format(i), dpi=80)

images = []
count = 0
for i in range(62):
    images.append(imageio.imread('/tmp/page_{}.png'.format(i)))
imageio.mimsave("Category.gif", images, fps=5)