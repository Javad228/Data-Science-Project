import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Get folder for data
inputdir = 'data\original'

####################
# Read in datasets #
####################

steps = pd.read_csv(f'{inputdir}/dailySteps_merged.csv')
steps.rename({'ActivityDay':'Date'},axis=1,inplace=True)
steps['Date'] = pd.to_datetime(steps['Date']).dt.date
steps.set_index(['Id','Date'],inplace=True)

sleep = pd.read_csv(f'{inputdir}/sleepDay_merged.csv')
sleep.rename({'SleepDay':'Date'},axis=1,inplace=True)
sleep['Date'] = pd.to_datetime(sleep['Date'],format='%m/%d/%Y %I:%M:%S %p').dt.date
sleep['HoursAsleep']=sleep['TotalMinutesAsleep']/60
sleep.drop(['TotalSleepRecords','TotalTimeInBed','TotalMinutesAsleep'],axis=1,inplace=True)
sleep.set_index(['Id','Date'],inplace=True)
sleep.drop_duplicates(inplace=True)

mets = pd.read_csv(f'{inputdir}/minuteMETsNarrow_merged.csv')
mets.rename({'ActivityMinute':'Date'},axis=1,inplace=True)
mets['Date'] = pd.to_datetime(mets['Date'],format='%m/%d/%Y %I:%M:%S %p').dt.date
mets = mets.groupby(['Id','Date']).sum().reset_index()
mets.set_index(['Id','Date'],inplace=True)

intensity = pd.read_csv(f'{inputdir}/dailyIntensities_merged.csv')
intensity.rename({'ActivityDay':'Date'},axis=1,inplace=True)
intensity['Date'] = pd.to_datetime(intensity['Date']).dt.date
intensity.set_index(['Id','Date'],inplace=True)

calories = pd.read_csv(f'{inputdir}/dailyCalories_merged.csv')
calories.rename({'ActivityDay':'Date'},axis=1,inplace=True)
calories['Date'] = pd.to_datetime(calories['Date']).dt.date
calories.set_index(['Id','Date'],inplace=True)

heartrate = pd.read_csv(f'{inputdir}/heartrate_seconds_merged.csv')
heartrate.rename({'Time':'Date','Value':'Heartrate'},axis=1,inplace=True)
heartrate['Date'] = pd.to_datetime(heartrate['Date'],format='%m/%d/%Y %I:%M:%S %p').dt.date
heartrate = heartrate.groupby(['Id','Date']).mean().reset_index()
heartrate.set_index(['Id','Date'],inplace=True)

activity = pd.read_csv(f'{inputdir}/dailyActivity_merged.csv')
activity.rename({'ActivityDate':'Date'},axis=1,inplace=True)
activity['Date'] = pd.to_datetime(activity['Date']).dt.date
activity.set_index(['Id','Date'],inplace=True)

weight = pd.read_csv(f'{inputdir}/weightLogInfo_merged.csv')
weight['Date'] = pd.to_datetime(weight['Date'],format='%m/%d/%Y %I:%M:%S %p').dt.date
weight.drop(['WeightKg','WeightPounds','Fat','IsManualReport','LogId','BMI'],axis=1,inplace=True)
weight.set_index(['Id','Date'],inplace=True)

#################################
# Concatenate datasets together #
#################################

data = pd.concat([steps,sleep,mets,intensity,calories,heartrate,activity,weight],axis=1)
# Return ID and Date to columns
data.reset_index(inplace=True)

# Remove duplicate columns
data = data.loc[:,~data.columns.duplicated()].copy()
# Remove observations where there is no sleep observation
data.dropna(subset=['HoursAsleep'],inplace=True)

# Create indicator for weekday (0) or weekend (1)
data['weekend'] = pd.to_datetime(data['Date']).dt.weekday
# Monday = 0, ..., Saturday = 5, Sunday = 6.
data['weekend'] = data['weekend'] > 4

# Split the dataset into training and testing sets.
X_train, X_test, y_train, y_test = train_test_split(data.drop('HoursAsleep',axis=1),
                                                    data['HoursAsleep'],
                                                    test_size=0.2,
                                                    random_state=0)

X_train.to_csv('data/clean/X_train.csv',index=False)
X_test.to_csv('data/clean/X_test.csv',index=False)
y_train.to_csv('data/clean/y_train.csv',index=False)
y_test.to_csv('data/clean/y_test.csv',index=False)
