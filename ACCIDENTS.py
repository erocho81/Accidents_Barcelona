#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


#Importacion de los datasets
#Dataset import

vehiculos = pd.read_csv('E:/Análisis de datos/DATASETS/BCN accidentes/Accidentes vehiculos TOTAL.csv')
                     
personas = pd.read_csv('E:/Análisis de datos/DATASETS/BCN accidentes/Accidents personas TOTAL.csv')

tipos = pd.read_csv('E:/Análisis de datos/DATASETS/BCN accidentes/Accidents tipos TOTAL.csv')

cantidades = pd.read_csv('E:/Análisis de datos/DATASETS/BCN accidentes/Accidents cantidad vehiculos y victimas TOTAL.csv')

causas= pd.read_csv('E:/Análisis de datos/DATASETS/BCN accidentes/Accidentes causas TOTAL.csv')


#Revisamos uno de los datasets
#We check one of the datasets
vehiculos.head()


# In[2]:


#Revisamos las columnas de un dataset
#We check its columns
vehiculos.columns


# In[3]:


#Revisamos las columnas de otro de los datasets.
#We also check the columns of the next dataset.
personas.columns


# In[4]:


#Eliminamos columnas que coinciden con el primer dataset.
#We will be deleting the columns that match this dataset with the previous one.
personas = personas.drop(columns=['Codi districte', 'Nom districte', 'Codi barri',
       'Nom barri', 'Codi carrer', 'Nom carrer', 'Nom Carrer 2',
       'Num postal caption', 'Descripció dia setmana', 'Dia setmana',
       'Descripció tipus dia', 'NK Any', 'Mes de any', 'Nom mes', 'Dia de mes',
       'Descripció torn', 'Hora de dia', 'Data completa',
       'Descripció causa vianant', 'Coordenada UTM (Y)',
       'Coordenada UTM (X)', 'Longitud', 'Latitud'])


# In[5]:


#Volvemos a revisar:
#We check the columns again:
personas.columns


# In[6]:


#Haremos lo mismo con el resto de datasets.
#We will be doing the same with the rest of the datasets:
tipos.columns


# In[7]:


tipos = tipos.drop(columns=['Codi districte', 'Nom districte', 'Codi barri',
       'Nom barri', 'Codi carrer', 'Nom carrer', 'Nom Carrer 2',
       'Num postal caption', 'Descripció dia setmana', 'Dia setmana',
       'Descripció tipus dia', 'NK Any', 'Mes de any', 'Nom mes', 'Dia de mes',
       'Data completa', 'Hora de dia', 'Descripció torn','Coordenada UTM (Y)', 'Coordenada UTM (X)',
       'Longitud', 'Latitud'])


# In[8]:


tipos.columns


# In[9]:


cantidades.columns


# In[10]:


cantidades = cantidades.drop(columns=['Codi districte', 'Nom districte', 'NK barri',
       'Nom barri', 'Codi carrer', 'Nom carrer', 'Nom carrer 2',
       'Num postal caption', 'Descripció dia setmana', 'Dia de setmana',
       'Descripció tipus dia', 'NK Any', 'Mes de any', 'Nom mes', 'Dia de mes',
       'Data completa', 'Hora de dia', 'Descripció torn',
       'Descripció causa vianant','Coordenada UTM (Y)', 'Coordenada UTM (X)', 'Longitud', 'Latitud'])


# In[11]:


cantidades.columns


# In[12]:


causas.columns


# In[13]:


causas = causas.drop(columns=['Codi districte', 'Nom districte', 'Codi barri',
       'Nom barri', 'Codi carrer', 'Nom carrer', 'Nom carrer 2',
       'Num postal caption', 'Descripció dia setmana', 'Dia setmana',
       'Descripció tipus dia', 'NK Any', 'Mes de any', 'Nom mes', 'Dia de mes',
       'Data Completa', 'Hora de dia', 'Descripció torn',
      'Coordenada UTM (Y)', 'Coordenada UTM (X)',
       'Longitud', 'Latitud'])


# In[14]:


causas.columns


# In[15]:


#Unimos los datasets
#We join the datasets.
accidents = pd.merge(personas,vehiculos, how='inner', on=["Codi expedient"])


# In[16]:


accidents = pd.merge(accidents,tipos, how='inner', on=["Codi expedient"])


# In[17]:


accidents = pd.merge(accidents,cantidades, how='inner', on=["Codi expedient"])


# In[18]:


accidents = pd.merge(accidents,causas, how='inner', on=["Codi expedient"])


# In[19]:


#Revisamos el nuevo dataset creado a partir de los joins anteriores
#We check the new dataset create by joining the previous ones.
accidents.columns


# In[20]:


accidents.head()


# In[21]:


accidents.dtypes


# In[22]:


#Cambiamos los nombres de las columnas añadiendo _ paras que sea más sencillo manipularlas
#Column name changes to include _

accidents.columns = accidents.columns.str.replace(' ','_')
accidents.dtypes


# In[23]:


#Cambiamos NA por 0 para poder cambiar el tipo de datos de las columnas después, 
#ya que necesitamos que algunos de ellos sean int para hacer calculos posteriores

#We change NA's to 0, to be able to change the data type for some of the columns,
#since we need to make some calculations with them later:

accidents = accidents.fillna(0)


# In[24]:


accidents.Edat= accidents.Edat.astype('int')


# In[25]:


accidents.NK_Any= accidents.NK_Any.astype('int')


# In[26]:


accidents.Mes_de_any= accidents.Mes_de_any.astype('int')


# In[27]:


accidents.Dia_de_mes= accidents.Dia_de_mes.astype('int')


# In[28]:


accidents.Codi_districte= accidents.Codi_districte.astype('int')


# In[29]:


accidents.Codi_barri= accidents.Codi_barri.astype('int')


# In[30]:


accidents.Codi_carrer= accidents.Codi_carrer.astype('int')


# In[31]:


accidents.dtypes


# In[32]:


#En caso de que queramos eliminar los valores nulls según un umbral determinado:
#In case we wanted to delete some of the null values

total = accidents.isnull().sum().sort_values(ascending=False)
percent = (accidents.isnull().sum()/accidents.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data[missing_data['Total'] > 0]


# In[33]:


#Sin embargo en este caso no funcionará, ya que ya hemos cambiado los valores, 
#y porque los valores no están dentro de los márgenes establecidos en el siguiente código:

#In this case it won't work, we have already changed the values to 0 and also, 
#there would not be values inside the margins set below:

accidents = accidents[missing_data[missing_data['Percent'] < 0.15].index]

accidents


# In[34]:


#Realizamos una visualización rápida de los valores numéricos:
#Quick viz of all numeric values:

accidents.hist(bins=50, figsize=(30,20));


# In[35]:


#Podemos visualizar solo algunas de las columnas:
#Viz for some of the columns:
accidents.hist(bins=50, figsize=(30,20), column=["Antiguitat_carnet", "Codi_districte", "Codi_carrer", "Codi_barri", "Mes_de_any", "NK_Any"])


# In[36]:


#Revisamos medias, ds, min, max, quantiles:
#Average, median, min, max and quantiles:
accidents.describe().T


# In[37]:


accidents.describe()


# In[38]:


#También podemos hacerlo para algun quantil determinado, etc:
#Showing only a quantile:
accidents.quantile(0.25)


# In[39]:


#O podemos revisar solo una de las columnas:
#Checking only one of the columns:

accidents["Antiguitat_carnet"].describe()


# In[40]:


accidents["Antiguitat_carnet"].hist()


# In[42]:


#Cantidad de expedientes (únicos) con víctimas:
#Total amount of expedients (unique) with victims:
Victimas = accidents.groupby("Número_de_víctimes").Codi_expedient.nunique()
print(Victimas)


# In[43]:


#Plot de las victimas calculadas antes
#Plot for victims/count of unique exp

ax = Victimas.plot(kind = 'bar')
ax.set_ylabel('Cantidad Exp por num de Victimas')


# In[44]:


#Cantidad de victimas por año:
#Totl amount of victims per year:

accidents.groupby('NK_Any')['Número_de_víctimes'].agg(['sum'])


# In[45]:


#Subset, filtro con muertos y graves menores de 30 años
#Subset and filter with dead and sever injured under 30 years of age:

Morts_Greus_Edat = accidents[(accidents.Descripció_victimització == "Mort") | 
                             (accidents.Descripció_victimització == "Ferit Greu") & (accidents.Edat<30)]
Morts_Greus_Edat.head()


# In[46]:


#Media de víctimas según Edat:
#Average victimes per age:

accidents[['Edat', 'Número_de_víctimes']].groupby(['Edat'], as_index=False).mean()


# In[47]:


#Aplicamos el test de normalidad al número de víctimas.
#Normality test applied to victims.

from scipy.stats import norm
sns.distplot(accidents['Número_de_víctimes'], fit = norm)


# In[48]:


#Calculamos el coeficiente de asimetria. Al ser mayor de 1, los valores son más densos hacia la izquierda del gráfico.
#En una distribución normal, el valor debería acercarse a 0.

#Asymetry coefficient for victims. Since it's larger than 1, values are more dense to the left. 
#On a normal distribution, the value should be closer to 0.

accidents['Número_de_víctimes'].skew()


# In[49]:


#Calculamos el valor kurtosis para averiguar la relación del pico central con los extremos de la campana de distribución.
#El valor debería ser cercano a 1 para ser coherente con la normalidad de la variable. 

#Kurtosis value calculation to check the relationship between the central peak with the far ends of the distribution bell.
#The value should be colse to 1 to be consistent with the normality of the variable.

accidents['Número_de_víctimes'].kurt()


# In[50]:


#Si tenemos una variable que no es normal, debemos aplicar el logaritmo a la variable:
#We apply the log to make "Numero de victimes" reach normality.

accidents['Número_de_víctimes'] = np.log1p(accidents['Número_de_víctimes'])
sns.distplot(accidents['Número_de_víctimes'], fit = norm)


# In[51]:


#Comprobamos si la variable ha sido normalizada:
#We check the previous values again:

accidents['Número_de_víctimes'].skew()


# In[52]:


accidents['Número_de_víctimes'].kurt()


# In[53]:


#Vamos a revisar a continuación variables categóricas:
#Let's check now categorical values:
accidents["Descripció_tipus_de_vehicle"].value_counts().plot(kind='bar')


# In[54]:


#Realizaremos ahora un análisis bivariante entre "Antiguitat Carnet" y "Número de víctimes".
#Now a bivariant check between "Antiguitat Carnet" and "Número de víctimes".

var = 'Antiguitat_carnet'
data = pd.concat([accidents['Número_de_víctimes'], accidents['Antiguitat_carnet']], axis=1)
data.plot.scatter(x='Antiguitat_carnet', y='Número_de_víctimes')


# In[55]:


#Analizamos variables categóricas
#Another check of categorical values:

var = 'Descripció_dia_setmana'
data = pd.concat([accidents['Número_de_víctimes'], accidents[var]], axis=1)
f, ax = plt.subplots(figsize=(16, 8))
fig = sns.boxplot(x=var, y='Número_de_víctimes', data=data)
plt.xticks(rotation=90);


# In[56]:


#Revisamos relaciones cruzadas entre varias variables a la vez:
#We check crossed relationships between some variables:

sns.set()
cols = ['Edat', 'Número_de_vehicles_implicats','Número_de_morts',
                     'Número_de_lesionats_greus']
sns.pairplot(accidents[cols], height = 2.5)
plt.show();


# In[57]:


#Vamos a crear un dataframe para hacer una correlacion pero solo de las columnas que nos interesan de accidents:
#We create a new dataframe to correlate some of the columns we are interested in:

acc_corr= accidents[['Edat', 'Número_de_víctimes','Dia_de_mes', 'Antiguitat_carnet',
                     'Número_de_vehicles_implicats','Número_de_morts',
                     'Número_de_lesionats_lleus','Número_de_lesionats_greus']]
acc_corr.head()


# In[58]:


#Creamos la representación de la correlación.
#We create the visual representation of the correlation.

correlation_matrix = acc_corr.corr()
correlation_matrix

plt.figure(figsize=(14,12))
plt.title('Pearson Correlation of Features', y=1.05, size=15)
sns.heatmap(correlation_matrix, annot=True);

#A parte de la correlación entre distrito-barrio, lesionados leves-victimas, vemos que las 
#correlaciones son más altas para Edad-Antiguitat_Carnet,Num_de_Victimes-Num_vehicles_implicats, 
#y lesionats lleus-vehicles implicats 

#We can see some obviuos correlations between distrito-barrio, lesionados leves-victimas, but also between 
# Edad-Antiguitat_Carnet,Num_de_Victimes-Num_vehicles_implicats and y lesionats lleus-vehicles implicats .


# In[59]:


#Realizaremos el mismo estudio en otro formato:
#Another way of creating a similar study:

corrmat = accidents.corr(method='spearman')
f, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corrmat, ax=ax, cmap="YlGnBu", linewidths=0.1)


# In[62]:


#Revisamos solo las 5 var más relacionadas con "Numero de victimes".
#We can also check the 5 variables most related with "Numero de victimes".

k = 5
cols = corrmat.nlargest(k, 'Número_de_víctimes')['Número_de_víctimes'].index
cm = np.corrcoef(accidents[cols].values.T)
f, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(cm, ax=ax, cmap="YlGnBu", linewidths=0.1, yticklabels=cols.values, xticklabels=cols.values)

