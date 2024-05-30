# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name:Awinenyam Kojo Stephen 
# Collaborators (discussion):Awinenyam Kojo Stephen
# Time: 6:00 pm 24th May,2024

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    x = pylab.array(x)
    y = pylab.array(y)

    coeff = []

    for i in degs:
        coeff.append(pylab.polyfit(x,y,i))

    return coeff     



def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    num = sum((y-estimated)**2)
    mean = sum(y)/len(y)
    deno = sum((y-mean)**2)

    return 1-num/deno
    

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.
    Returns:
        None
    """
    rSquare = []
    for i in models:
        estimated = pylab.polyval(i,x)
        rSquare.append(r_squared(y,estimated))
        if min(rSquare):
           if len(i)==2:
               SE=se_over_slope(x,y,estimated,i)
               pylab.plot(x,estimated,'r-',label='degree of regression='+str(len(i)-1)+'R SQUARED ='+str(rSquare)+'se over slope='+str(SE))
               pylab.figure()
           else:
               pylab.plot(x,estimated,'r-',label='degree of regression='+str(len(i)-1)+'R SQUARED ='+str(rSquare))
               pylab.figure() 
        else:
            if len(i)==2:
               SE=se_over_slope(x,y,estimated,i)
               pylab.plot(x,estimated,'b--',label='degree of regression='+str(len(i)-1)+'R SQUARED ='+str(rSquare)+'se over slope='+str(SE))
               pylab.figure()
            else:
               pylab.plot(x,estimated,'b--',label='degree of regression='+str(len(i)-1)+'R SQUARED ='+str(rSquare))
               pylab.figure() 


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    anual_average = []
    for year in years:
        average = []
        for city in multi_cities:
            temp = climate.get_yearly_temp(city,year)
            total = sum(temp)/len(temp)
            average.append(total)
        anual_average.append(sum(average)/len(average))    
    return pylab.array(anual_average)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    y = list(y)
    k = y.copy()
    moved = []
    average = 0

    for index,x in enumerate(k):
        if (index+1) <= window_length:
            average += x
            moved.append(average/(index+1))
        else:
            pop = y.pop(window_length - window_length)
            average -= pop
            average += x
            moved.append(average/(window_length))
            
    return pylab.array(moved)        
     
def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    y = list(y)
    estimated = list(estimated)
    num = 0

    for i in range(len(estimated)):
        num += (y[i]-estimated[i])**2

    return (num/len(y))**0.5    

def gen_std_devs(climate, multi_cities, years):
    """ 
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    
    STD = []

    for year in years:
        daily_temp1 = [0]*366
        average = []
        for city in multi_cities:
            temp = climate.get_yearly_temp(city,year)
            daily_temp1.append(temp)
        total = sum(daily_temp1)
        for i in total:
            average.append(i/len(multi_cities))    
        yearly_average = sum(average)/len(average)
        num = 0
        for i in range(len(average)):
            num += (average[i]-yearly_average)**2
        STD.append((num/len(average))**0.5)

    return pylab.array(STD)      

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        estimated=pylab.polyval(model,x)
        RMSE=rmse(y,estimated)
        if min(RMSE):
            pylab.plot(x,estimated,'r-',label="degree ="+str(len(model))+"RMSE ="+str(RMSE))
        else:
            pylab.plot(x,estimated,'b--',label="degree ="+str(len(model))+"RMSE ="+str(RMSE))



if __name__ == '__main__':

    # Part A.4 I
    # y = []
    # for year in TRAINING_INTERVAL:
    #     climate = Climate('data.csv')
    #     y.append(climate.get_daily_temp("NEW YORK",1,10,year))
    # y = pylab.array(y)
    # x = pylab.array(TRAINING_INTERVAL)    
    # model=generate_models(x,y,[1]) 
    # evaluate_models_on_training(x,y,model)
    # evaluate_models_on_training(x,y,model)    

    # # Part B
    # x = pylab.array(TESTING_INTERVAL)
    # y = gen_cities_avg(climate,CITIES,TESTING_INTERVAL)
    # model=generate_models(x,y,[1])
    # evaluate_models_on_training(x,y,model)

    # # Part C
    # x = pylab.array(TRAINING_INTERVAL)
    # y = moving_average(x,5)
    # model = generate_models(x,y,[1])
    # evaluate_models_on_testing(x,y,model)

    # # Part D.2
    # x = pylab.array(TRAINING_INTERVAL)
    # y = moving_average(x,5)
    # model = generate_models(x,y,[1,2,20])
    # evaluate_models_on_training(x,y,model)

    # # Part D.2 II
    # x = pylab.array(TRAINING_INTERVAL)
    # y = moving_average(x,5)
    # model = generate_models(x,y,[1,2,20])
    # evaluate_models_on_training(x,y,model)

    # # Part E
    # x = pylab.array(TESTING_INTERVAL)
    # y = gen_std_devs(climate,CITIES,x)
    # yVal = moving_average(y,5)
    # model = generate_models(x,y,[1])
    # evaluate_models_on_testing(x,yVal,model)
    
    pass