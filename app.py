import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# MUST come first
df = pd.read_csv("ACCIDENTDATA_PROJECT_UNIQUE_IMAGES.csv")  # <-- your file name here

st.title("Road Accident Severity Dashboard")

# Now you can safely use df
severity_counts = df['Severity_Label'].value_counts().reindex(['Slight', 'Severe', 'Fatal'])

fig, ax = plt.subplots()
sns.barplot(x=severity_counts.index, y=severity_counts.values, ax=ax)
st.pyplot(fig)




severity_counts = df['Severity_Label'].value_counts().reindex(['Slight', 'Severe', 'Fatal'])
total = severity_counts.sum()
percentages = (severity_counts / total) * 100

plt.figure(figsize=(8,5))
sns.barplot(x=severity_counts.index, y=severity_counts.values, palette="viridis")

plt.title("Distribution of Road Accidents by Severity", fontsize=14)
plt.xlabel("Accident Severity", fontsize=12)
plt.ylabel("Number of Accidents", fontsize=12)

for i, (count, pct) in enumerate(zip(severity_counts.values, percentages)):
    plt.text(i, count, f"{count:,}\n({pct:.1f}%)", 
             ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()


fatal_df = df[df['Severity_Label'] == 'Fatal']


fatal_speed_counts = fatal_df['Speed_Group'].value_counts().reindex(['Low (≤30)', 'Medium (40–50)', 'High (60+)'])


plt.figure(figsize=(8,5))
sns.barplot(x=fatal_speed_counts.index, y=fatal_speed_counts.values, palette='Reds')

plt.title("Fatal Accidents by Speed Limit Category", fontsize=14)
plt.xlabel("Speed Limit Category", fontsize=12)
plt.ylabel("Number of Fatal Accidents", fontsize=12)


for i, v in enumerate(fatal_speed_counts.values):
    plt.text(i, v, f"{v:,}", ha='center', va='bottom')

plt.tight_layout()
plt.show()

day_counts = df['Day_Period'].value_counts()


plt.figure(figsize=(7,7))
plt.pie(day_counts, 
        labels=day_counts.index, 
        autopct='%1.1f%%', 
        startangle=90,
        colors=['#1f77b4','#ff7f0e','#2ca02c','#d62728'])

plt.title("Percentage of Accidents by Time of Day", fontsize=14)
plt.tight_layout()
plt.show()

heat = pd.crosstab(df['Day_Period'], df['Severity_Label'], normalize='columns') * 100

plt.figure(figsize=(7,4))
sns.heatmap(heat,
            annot=True,
            fmt=".1f",
            cmap="Reds",
            linewidths=0.5,
            cbar_kws={'label': 'Percentage of Accidents'})

plt.title("When Do Accidents Happen?", fontsize=14)
plt.xlabel("Severity Level")
plt.ylabel("Time of Day")

plt.tight_layout()
plt.show()

df['Env_Condition'] = df['Weather_Report'] + " | " + df['Light_Report']

combo = pd.crosstab(df['Env_Condition'], df['Severity_Label'], normalize='columns') * 100


plt.figure(figsize=(8,6))
sns.heatmap(combo,
            annot=True,
            fmt=".1f",
            cmap="magma",
            linewidths=0.5,
            cbar_kws={'label': 'Percentage of Accidents'})

plt.title("When Do Severe Accidents Happen? Weather + Lighting", fontsize=14)
plt.xlabel("Severity Level")
plt.ylabel("Environmental Condition")

plt.tight_layout()
plt.show()

hour_counts = df['Hour'].value_counts().sort_index()


plt.figure(figsize=(10,4))
sns.lineplot(x=hour_counts.index, y=hour_counts.values, marker='o')

plt.title("Accidents by Hour of Day", fontsize=14)
plt.xlabel("Hour of Day (0–23)")
plt.ylabel("Number of Accidents")
plt.xticks(range(0,24))
plt.tight_layout()
plt.show()


print("Top 5 hours with most accidents:")
print(hour_counts.sort_values(ascending=False).head(5))

road_severity = pd.crosstab(df['Road_Type'], df['Severity_Label'], normalize='index') * 100
road_severity = road_severity.reset_index().melt(id_vars='Road_Type',
                                                var_name='Severity',
                                                value_name='Percentage')

plt.figure(figsize=(9,5))
sns.barplot(data=road_severity,
            x='Road_Type',
            y='Percentage',
            hue='Severity',
            palette=['#1b5e20','#e65100','#b71c1c'])

plt.title("Accident Severity Distribution by Road Type", fontsize=14)
plt.xlabel("Road Type")
plt.ylabel("Percentage of Accidents")
plt.xticks(rotation=45, ha='right')
plt.legend(title="Severity")
plt.tight_layout()
plt.show()

area_severity = pd.crosstab(df['Urban_or_Rural_Area'], df['Severity_Label'], normalize='index') * 100
area_severity = area_severity.reset_index().melt(id_vars='Urban_or_Rural_Area',
                                                var_name='Severity',
                                                value_name='Percentage')

plt.figure(figsize=(7,5))
sns.barplot(data=area_severity,
            x='Urban_or_Rural_Area',
            y='Percentage',
            hue='Severity',
            palette=['#1b5e20','#e65100','#b71c1c'])

plt.title("Accident Severity: Urban vs Rural Areas", fontsize=14)
plt.xlabel("Area Type")
plt.ylabel("Percentage of Accidents")
plt.legend(title="Severity")
plt.tight_layout()
plt.show()

vehicle_severity = pd.crosstab(df['Vehicle_Group'], df['Severity_Label'], normalize='index') * 100
vehicle_severity = vehicle_severity.reset_index().melt(id_vars='Vehicle_Group',
                                                      var_name='Severity',
                                                      value_name='Percentage')

plt.figure(figsize=(8,5))
sns.barplot(data=vehicle_severity,
            x='Vehicle_Group',
            y='Percentage',
            hue='Severity',
            palette=['#00897B', '#FFB300', '#C62828'])

plt.title("Accident Severity by Number of Vehicles Involved", fontsize=14)
plt.xlabel("Vehicle Involvement")
plt.ylabel("Percentage of Accidents")
plt.legend(title="Severity")
plt.tight_layout()
plt.show()

year_counts = df['Year'].value_counts().sort_index()

plt.figure(figsize=(8,4))
sns.lineplot(x=year_counts.index, y=year_counts.values, marker='o')

plt.title("Trend of Road Accidents Over the Years", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Accidents")
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

print(year_counts)

