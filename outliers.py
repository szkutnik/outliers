import random
import numpy as np
import pandas as pd
import scipy
from scipy.stats import t
from matplotlib import pyplot as plt


class outlier:
    
    def __init__(self, series):
        self.series = series


    
    def esd_test(self, k=10, alpha=0.05):
        
        
        """
        
        import random
        import numpy as np
        import pandas as pd
        import scipy
        from scipy.stats import t
        from matplotlib import pyplot as plt


        ## Defining the cases: 
        r = [random.normalvariate(0,1) for i in range(100)]
        
        ## The following example is borrowed from: https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h3.htm

        z = [-0.25, 0.68, 0.94, 1.15, 1.20, 1.26, 1.26,
              1.34, 1.38, 1.43, 1.49, 1.49, 1.55, 1.56,
              1.58, 1.65, 1.69, 1.70, 1.76, 1.77, 1.81,
              1.91, 1.94, 1.96, 1.99, 2.06, 2.09, 2.10,
              2.14, 2.15, 2.23, 2.24, 2.26, 2.35, 2.37,
              2.40, 2.47, 2.54, 2.62, 2.64, 2.90, 2.92,
              2.92, 2.93, 3.21, 3.26, 3.30, 3.59, 3.68,
              4.30, 4.64, 5.34, 5.42, 6.01]

        df = pd.DataFrame.from_dict({'x':r[:54], 'y':r[46:], 'z':z})
        df = df.set_index(pd.date_range("2018-01-01", periods=54, freq="Q"))

        s1 = df.loc[:,'x']
        s2 = df.loc[:,'y']
        s3 = df.loc[:,'z']


        ## Testing:
        ### ESD outlier test: 
        outliers = outlier(s3)

        esd1 = outliers.esd_test()
        esd2 = outliers.esd_test(k=5, alpha=0.3)

        ## see metadata attribute 
        esd1.describe()
        esd1.outliers.attrs

        ## see the plot
        esd1.plot()
        """
        
        
        series = self.series
        
        Ri = {}
        n = len(series)

        for j in range(0,k):

            i = j+1

            max_series = abs(series - series.mean())
            idx_remove = max_series.idxmax()

            index = list(series.index)[j]

            p = 1 - (alpha)/(2*(n-i+1))
            tval = t.ppf(p, n-i-1)

            lambda_i = (n - i)*tval/np.sqrt( (n - i -1  + tval**2 )*(n-i+1))

            ri = max_series.max()/series.std()

            Ri.update({idx_remove:(ri, lambda_i, ri>lambda_i)})

            series = series.drop([idx_remove])

        esd_output = pd.DataFrame.from_dict(Ri, orient='index')

        esd_output.rename(columns = {0:"Ri" ,1:"lambda" ,2:"Outlier" }, inplace = True) 
        
        output = pd.concat([self.series, esd_output], axis =1 )

        
        return esd_test(output, k, alpha, var_name = series.name)  
    
    
    
    


class esd_test():
    
    def __init__(self, outliers,k,alpha, var_name):
        self.outliers = outliers
        self.k = k 
        self.alpha = alpha
        self.var_name = var_name
        self.table = table(self)

    def table(self):

        table = self.outliers.query("not Outlier.isnull()")

        return table
        
        
    def plot(self, **kwargs):

        df = copy.deepcopy(self.outliers)


        df['color'] = df.loc[:,'Outlier'].map({np.nan: 'blue', True:'red', False:'green'})
        ax = df.plot(kind='bar', y=self.var_name, legend= False, color = df.color)

        ox = [dt.strftime('%y-%m-%d') if dt.month ==12 else '' for dt in df.index]

        ax.set_xticklabels(ox)
        
        ax.attrs={"metadata":{
            "caption": "Generalized ESD Test for Outliers for variable: "+str(self.var_name)+". Green and red bars indicate the status of the test stistic Ri.",
            "description": "The green (red) bars indicate the cases in which the unusual observations were not identified (identified)."
        }}
        
        plt.show()

        return ax
    
    def describe(self,**kwargs):
        
        output = self.outliers
        
        table_of_outliers = output.query('Outlier == True')
        n_of_outliers = table_of_outliers.shape[0]
        index_of_outliers = table_of_outliers.index
        
        table_of_nonan = output.query('Outlier in [True,False]')
        
        var_name = output.columns[0]
        
        if n_of_outliers>0:
            
            outcome_comment1 = " ".join([
                "The test showed that the number of outliers is",
                str(n_of_outliers), 
                "at a ",
                str(self.alpha),
                "level of significance.",
                "See details for cases:",
                ",".join([ str(i) for i in index_of_outliers])+".",
            ])
            
        else:
            outcome_comment1 = "The test showed no outliers."
            
        
        outcome_comment0 = "The occurrence of up to "+str(self.k)+" outliers in the "+str(self.var_name)+" variable was examined."
        

        output.attrs={"metadata":{
            
            "caption": f"Generalized ESD Test for Outliers for variable: {var_name}",
            "desription": "The generalized (extreme Studentized deviate) ESD test (Rosner 1983) is used to detect one or more outliers in a univariate data set that follows an approximately normal distribution.",
            "outcome": f"{outcome_comment0} {outcome_comment1}" ,            
            "outliers":{
                "name":var_name,
                "n_of_outliers":n_of_outliers,
                "index_of_outliers":index_of_outliers
            }}}
        
        return output.attrs
        
        
        

        
        
