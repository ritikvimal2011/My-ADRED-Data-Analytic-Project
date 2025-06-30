from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/energy-data")
def energy_data():
    df = pd.read_csv('Elctricsity_-capacity-statewise.csv')
    columns_to_plot = ['coal_cap', 'diesel_cap', 'nuclear_cap','gas_cap','lignite_cap','hydro_cap','res_cap']
    capacities = df[columns_to_plot].sum()
    labels = capacities.index
    values = capacities.values

    # Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Energy Capacity Distributions')
    plt.axis('equal')
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/energy_pie_chart.png')
    plt.close()

    # Bar Chart
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color='teal')
    plt.title('Total Capacity by Source')
    plt.xlabel('Source')
    plt.ylabel('Capacity')
    plt.tight_layout()
    plt.savefig('static/energy_bar_chart.png')
    plt.close()

    return render_template(
        "energy-data.html",
        graph1="energy_pie_chart.png",
        graph2="energy_bar_chart.png"
    )


@app.route("/railway-data")
def railway_data():
    # Load your dataset
    df = pd.read_csv('Train_details_22122017.csv')
    df.columns = df.columns.str.strip()
    df = df[['Station Code', 'Distance']].dropna()
    df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')
    chartxy = df.groupby('Station Code')['Distance'].max().reset_index()
    top_100 = chartxy.sort_values(by='Distance', ascending=False).head(100)

    # Plot 1: Top 100 Stations by Maximum Distance
    plt.figure(figsize=(14, 7))
    plt.plot(top_100['Station Code'], top_100['Distance'], color='navy')
    plt.xlabel('Station Code')
    plt.ylabel('Maximum Distance (km)')
    plt.title('Top 100 Stations by Maximum Distance')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('static/railway_chart1.png')
    plt.close()

    # Plot 2: Histogram of All Distances
    plt.figure(figsize=(10, 6))
    plt.hist(df['Distance'].dropna(), bins=30, color='orange', edgecolor='black')
    plt.xlabel('Distance (km)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Train Distances')
    plt.tight_layout()
    plt.savefig('static/railway_chart2.png')
    plt.close()

    # Plot 3: Number of Trains per Station (Top 20)
    train_counts = df['Station Code'].value_counts().head(20)
    plt.figure(figsize=(12, 6))
    train_counts.plot(kind='bar', color='green')
    plt.xlabel('Station Code')
    plt.ylabel('Number of Trains')
    plt.title('Top 20 Stations by Number of Trains')
    plt.tight_layout()
    plt.savefig('static/railway_chart3.png')
    plt.close()

    return render_template(
        "railway-data.html",
        graph1="railway_chart1.png",
        graph2="railway_chart2.png",
        graph3="railway_chart3.png"
    )

'''/* @app.route("/study-data")
def study_data():
    df = pd.read_csv('Study_data.csv')
    # ...process and plot...
    plt.figure()
    # ...your plotting code...
    plt.savefig('static/study_chart.png')
    plt.close()
    return render_template("study-data.html", graph="study_chart.png") 
*/'''

@app.route("/health-data")
def health_data():
    df = pd.read_csv('WHO-COVID-19-global-daily-data.csv')
    df_sampled_100 = df.sample(n=100, random_state=42)

    # Bar Chart: New Cases per Country
    plt.figure(figsize=(20, 8))
    plt.bar(df_sampled_100['Country'], df_sampled_100['New_cases'], color='skyblue')
    plt.xlabel('Country')
    plt.ylabel('New Cases')
    plt.title('New Cases per Country (Random 100 Rows Sample)')
    plt.xticks(rotation=90)
    plt.tight_layout()
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/health_chart.png')
    plt.close()

    # Line Chart: Cumulative Cases (for first 50 rows)
    df_sampled_50 = df.sample(n=50, random_state=42)
    plt.figure(figsize=(10, 5))
    plt.plot(df_sampled_50['Date_reported'], df_sampled_50['Cumulative_cases'], color='red')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Cases')
    plt.title('Cumulative Cases Over Time (Sample)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/health_line_chart.png')
    plt.close()

    return render_template(
        "health-data.html",
        graph1="health_chart.png",
        graph2="health_line_chart.png"
    )

@app.route("/wind-data")
def wind_data():
    chunk_iter = pd.read_csv('wind_file2012.csv', chunksize=100000, low_memory=True)
    for chunk in chunk_iter:
        df = chunk.copy()
        break

    df.columns = df.columns.str.strip()
    df['uwnd'] = pd.to_numeric(df['uwnd'], errors='coerce')

    # Histogram
    plt.figure(figsize=(10, 5))
    plt.hist(df['uwnd'].dropna(), bins=30, color='skyblue', edgecolor='black')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Wind Speed (First Chunk)')
    plt.tight_layout()
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/wind_chart.png')
    plt.close()

    # Boxplot
    plt.figure(figsize=(6, 5))
    plt.boxplot(df['uwnd'].dropna())
    plt.title('Wind Speed Boxplot')
    plt.ylabel('Wind Speed (m/s)')
    plt.tight_layout()
    plt.savefig('static/wind_boxplot.png')
    plt.close()

    return render_template(
        "wind-data.html",
        graph1="wind_chart.png",
        graph2="wind_boxplot.png"
    )



@app.route("/Platform_info")
def platform_info():
    return render_template("Platform_info.html")

if __name__ == "__main__":
    app.run(debug=True)
