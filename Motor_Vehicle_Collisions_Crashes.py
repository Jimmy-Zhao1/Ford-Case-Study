### Import packages in the virtual environment
import pandas as pd   ## search the package "pandans"
import statsmodels.api as sm    ## search the package "statsmodels"
import statsmodels.stats.api as sms   ## no need to install package
from statsmodels.compat import lzip  ## no need to install package
import matplotlib.pyplot as plt   ## search the package "matplotlib"
import seaborn as sns   ## search the package "seaborn"
import scipy.stats as scipy   ## search the package "scipy"
from scipy.stats import shapiro   ## no need to install package
import sys    ## no need to install package
import os     ## no need to install package
script_dir = script_dir = os.path.dirname(os.path.abspath(__file__))
file_path =  os.path.join(script_dir, "[Cleaned]_Motor_Vehicle_Collisions_Crashes.xlsx")
pd.set_option('display.max_columns', 500)
## Display all columns when printing results
mydata = pd.read_excel(file_path)
## Remember to include “r” first inside the bracket.

output_path = os.path.join(script_dir, 'output.txt')
file = open(output_path, 'wt')
sys.stdout = file
## Open a text file and save all results into the text file

print(mydata.describe())
## Display summary statistics of the data

df = pd.DataFrame(mydata)
##Transform the dataset into two-dimensional, size-mutable, potentially heterogeneous tabular data

######################## Linear regression with only one independent variable
x = df['FORD?']
##Define the independent variables in the model
y = df['ANY_DEATH']
##Define the dependent variable in the model

# with statsmodels
x = sm.add_constant(x)  # adding a constant
##Add a constant in the regression model

model1 = sm.OLS(y, x).fit(cov_type='HC0')
##Fit the model using Heteroskedasticity-Robust Standard Errors
results_model1 = model1.summary()
print(results_model1)
##Output the results

df["predicted1"] = model1.predict(x)
##Caculate the predicted value of dependent variable based on the model

#sns.scatterplot(data=df, x="FORD?", y="predicted1")
#plt.show()



######################## Linear regression with only multiple independent variables

x = df[['FORD?', 'NIGHT_TIME', 'VEHICLE_YEAR', 'OCCUPANTS', 
            'DRIVER_LICENSE_STATUS', 'STATE_REGISTRATION_MISSING',
            'NORTH_DRIVER_LICENSE', 'MIDWEST_DRIVER_LICENSE', 'WEST_DRIVER_LICENSE', 
            ]]
##Define the independent variables in the model
y = df['ANY_DEATH']
##Define t he dependent variable in the model

# with statsmodels
x = sm.add_constant(x)  # adding a constant
##Add a constant in the regression model

model2 = sm.OLS(y, x).fit(cov_type='HC0')
##Fit the model using Heteroskedasticity-Robust Standard Errors
results_model2 = model2.summary()
print(results_model2)
##Output the results

df["predicted2"] = model2.predict(x)
##Caculate the predicted value of dependent variable based on the model


#sns.scatterplot(data=df, x="FORD?", y="predicted2")
#plt.show()

##Regression diagnostic I: multicollinearity
corr_matrix = df.corr()
print(corr_matrix)

##Regression diagnostic 2: heteroscedasticity in the error term
names = ['Lagrange multiplier statistic', 'p-value',
        'f-value', 'f p-value']
test = sms.het_breuschpagan(model2.resid, model2.model.exog)
print(lzip(names, test))


##Regression diagnostic 3: autocorrelation
##This is not a time-series dataset. Thus, the concern about autocorrelation is minimal.

##Regression diagnostic 4: model specification errors
##1)The model does not exclude any “core” variables.
##2)The model does not include superfluous variables.
##3)The functional form of the model is suitably chosen.
##4)There are no errors of measurement in the regressand and regressors.
##5)Outliers in the data, if any, are taken into account.

print(mydata.describe())

##6)The probability distribution of the error term is well specified.
residuals = model2.resid
print(shapiro(residuals))

file.close()
##Close the text file.


