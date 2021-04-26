import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.widgets import CheckButtons

# Enter CSV to process:
word_count = pd.read_csv("data/Sample_csv.csv")

print(word_count)

professor = word_count[word_count['Speaker'] == 'A']
students = word_count[word_count['Speaker'] == 'B']
minute_A = professor['Minute']
speaker_A = professor['WPM']
minute_B = students['Minute']
speaker_B = students['WPM'] 

df1 = pd.DataFrame(speaker_A)
df1.columns =['AWPM'] 
df2 = pd.DataFrame(speaker_B)
df2.columns =['BWPM'] 

# Merge df1 and df2
result = pd.concat([df1, df2], axis=1)
result = result.reset_index(drop=False)

# Replace NaN values with zeroes:
result.fillna(0, inplace=True)
result = result.astype(int)


fig, (ax1, ax3) = plt.subplots(2)
ax1.plot(result['index'], result['AWPM'],color ='black',label = 'Professor')
ax1.set_title('Professor Word Count')
ax1.set_xlabel('Minutes')
ax1.set_ylabel('Word/Min')

ax2 = ax1.twinx()
ax2.set_ylabel('Attentiveness',color ='green')
ax2.tick_params(axis='y', colors='green')
ax2.plot(word_count['Minute'],word_count['Attentiveness'], color = 'green',label = 'Attentiveness')

ax3.plot(result['index'], result['BWPM'],color ='black',label = 'Students')
ax3 .set_title('Students Word Count')
ax3.set_xlabel('Minutes')
ax3.set_ylabel('Word/Min')

ax4 = ax3.twinx()
ax4.set_ylabel('Attentiveness',color ='green')
ax4.tick_params(axis='y', colors='green')
ax4.plot(word_count['Minute'],word_count['Attentiveness'], color = 'green',label = 'Attentiveness')

fig.tight_layout()
plt.show()



fig, ax5 = plt.subplots()
plt.grid()
plt.title('Ranked Complexity')
ax5.set_xlabel('Minutes')
ax5.set_ylabel('Ranked Complexity')
ax5.plot(result['index'], word_count['Ranked Complexity'])

ax6 = ax5.twinx()
ax6.set_ylabel('Attentiveness',color ='green')
ax6.tick_params(axis='y', colors='green')
ax6.plot(word_count['Minute'],word_count['Attentiveness'], color = 'green',label = 'Attentiveness')
plt.show()