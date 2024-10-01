import pandas as pd
import os

# Get folder for data
folder = 'data\original'

####################
# Read in datasets #
####################

steps = pd.read_csv(f'{folder}/dailySteps_merged.csv')
steps.rename({'ActivityDay':'Date'},axis=1,inplace=True)
steps['Date'] = pd.to_datetime(steps['Date']).dt.date
steps.set_index(['Id','Date'],inplace=True)

sleep = pd.read_csv(f'{folder}/sleepDay_merged.csv')
sleep.rename({'SleepDay':'Date'},axis=1,inplace=True)
sleep['Date'] = pd.to_datetime(sleep['Date'],format='%m/%d/%Y %I:%M:%S %p').dt.date
sleep['HoursAsleep']=sleep['TotalMinutesAsleep']/60
sleep.drop(['TotalSleepRecords','TotalTimeInBed'],axis=1,inplace=True)
sleep.set_index(['Id','Date'],inplace=True)
sleep.drop_duplicates(inplace=True)

mets = pd.read_csv(f'{folder}/minuteMETsNarrow_merged.csv')
mets.rename({'ActivityMinute':'Date'},axis=1,inplace=True)
mets['Date'] = pd.to_datetime(mets['Date'],format='%m/%d/%Y %I:%M:%S %p').dt.date
mets = mets.groupby(['Id','Date']).sum().reset_index()
mets.set_index(['Id','Date'],inplace=True)

intensity = pd.read_csv(f'{folder}/dailyIntensities_merged.csv')
intensity.rename({'ActivityDay':'Date'},axis=1,inplace=True)
intensity['Date'] = pd.to_datetime(intensity['Date']).dt.date
intensity.set_index(['Id','Date'],inplace=True)

calories = pd.read_csv(f'{folder}/dailyCalories_merged.csv')
calories.rename({'ActivityDay':'Date'},axis=1,inplace=True)
calories['Date'] = pd.to_datetime(calories['Date']).dt.date
calories.set_index(['Id','Date'],inplace=True)

heartrate = pd.read_csv(f'{folder}/heartrate_seconds_merged.csv')
heartrate.rename({'Time':'Date','Value':'Heartrate'},axis=1,inplace=True)
heartrate['Date'] = pd.to_datetime(heartrate['Date'],format='%m/%d/%Y %I:%M:%S %p').dt.date
heartrate = heartrate.groupby(['Id','Date']).mean().reset_index()
heartrate.set_index(['Id','Date'],inplace=True)

activity = pd.read_csv(f'{folder}/dailyActivity_merged.csv')
activity.rename({'ActivityDate':'Date'},axis=1,inplace=True)
activity['Date'] = pd.to_datetime(activity['Date']).dt.date
activity.set_index(['Id','Date'],inplace=True)

weight = pd.read_csv(f'{folder}/weightLogInfo_merged.csv')
weight['Date'] = pd.to_datetime(weight['Date'],format='%m/%d/%Y %I:%M:%S %p').dt.date
weight.drop(['WeightKg','WeightPounds','Fat','IsManualReport','LogId'],axis=1,inplace=True)
weight.set_index(['Id','Date'],inplace=True)

# Get shape of each dataset to get number of observations
print(steps.shape)
print(sleep.shape)
print(mets.shape)
print(intensity.shape)
print(calories.shape)
print(heartrate.shape)
print(activity.shape)
print(weight.shape)

# Concatenate datasets together
data = pd.concat([steps,sleep,mets,intensity,calories,heartrate,activity,weight],axis=1)
# Return ID and Date to columns
data.reset_index(inplace=True)
# Remove duplicate columns
data = data.loc[:,~data.columns.duplicated()].copy()

# Describe dataset
print(data.describe())
# Print names of columns
print(data.columns)
# Print correlation matrix for all the variables
print(data.drop(['Id','Date'],axis=1).corr())
