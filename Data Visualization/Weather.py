import csv
from matplotlib import pyplot as plt

# filename = 'C:\\spyder_mj\\project_01\\Chapter_01\\data_visualization\\sitka_weather_2014.csv'
# with open(filename) as f:
#    reader = csv.reader(f)
#    header_row = next(reader)

#    dates, highs, lows = [],[],[]
#    for row in reader:
#        current_date = datetime.strptime(row[0],'%Y-%m-%d')
#        dates.append(current_date)
#        highs.append(int(row[1]))
#        lows.append(int(row[3]))

#    #for index, column in enumerate(header_row):
#    #    print(index,column)

# fig = plt.figure(dpi = 128, figsize = (10,6))
# plt.plot(dates, highs, c='red', alpha = 0.5)
# plt.plot(dates, lows, c='blue', alpha = 0.5)
# plt.fill_between(dates, highs, lows, facecolor='blue', alpha = 0.1)
# plt.title('Daily high & low temperatures, 2014', fontsize =24)
# plt.xlabel('', fontsize = 8)
# fig.autofmt_xdate()
# plt.ylabel('Temp (F)', fontsize = 16)
# plt.tick_params(axis = 'both', which = 'major', labelsize = 10)

# plt.show()

from datetime import datetime

filename = 'C:\\spyder_mj\\project_01\\Chapter_01\\data_visualization\\death_valley_2014.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    dates, highs, lows = [], [], []
    for row in reader:
        try:
            current_date = datetime.strptime(row[0], '%Y-%m-%d')
            high = int(row[1])
            low = int(row[3])
        except ValueError:
            print(current_date, 'missing_data')
        else:
            dates.append(current_date)
            highs.append(high)
            lows.append(low)

    # for index, column in enumerate(header_row):
    #    print(index,column)

fig = plt.figure(dpi=128, figsize=(10, 6))
plt.plot(dates, highs, c='red', alpha=0.5)
plt.plot(dates, lows, c='blue', alpha=0.5)
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
plt.title('Daily high & low temperatures, 2014 \nDeath Valley', fontsize=24)
plt.xlabel('', fontsize=8)
fig.autofmt_xdate()
plt.ylabel('Temp (F)', fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=10)

plt.show()
