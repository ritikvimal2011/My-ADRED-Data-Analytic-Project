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
    # Step 1: Read the CSV
    df = pd.read_csv('Elctricsity_-capacity-statewise.csv')

    # Step 2: Choose relevant columns
    columns_to_plot = ['coal_cap', 'diesel_cap', 'nuclear_cap','gas_cap','lignite_cap','hydro_cap','res_cap']
    capacities = df[columns_to_plot].sum()
    labels = capacities.index
    values = capacities.values

    # Step 3: Create Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Energy Capacity Distributions')
    plt.axis('equal')

    # Step 4: Save image to static folder
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/energy_pie_chart.png')
    plt.close()

    # 👇 Add this line to check the actual save location
    print("Saving chart to:", os.path.abspath('static/energy_pie_chart.png'))

    # Step 5: Render HTML page
    return render_template("energy-data.html", graph="energy_pie_chart.png")


@app.route("/railway-data")
def railway_data():
    # Load your dataset
    df = pd.read_csv('Train_details_22122017.csv')
    df.columns = df.columns.str.strip()
    df = df[['Station Code', 'Distance']].dropna()
    df['Distance'] = pd.to_numeric(df['Distance'], errors='coerce')
    chartxy = df.groupby('Station Code')['Distance'].max().reset_index()
    top_100 = chartxy.sort_values(by='Distance', ascending=False).head(100)

    # Plotting
    plt.figure(figsize=(18, 7))
    plt.plot(top_100['Station Code'], top_100['Distance'], color='navy')
    plt.xlabel('Station Code')
    plt.ylabel('Maximum Distance (km)')
    plt.title('Top 100 Stations by Maximum Distance')
    plt.xticks(rotation=90)
    plt.tight_layout()
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/railway_chart.png')
    plt.close()

    print("Saving chart to:", os.path.abspath('static/railway_chart.png'))
    return render_template("railway-data.html", graph="railway_chart.png")

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
    max_new_cases_row = df_sampled_100.loc[df_sampled_100['New_cases'].idxmax()]

    # Plot New_cases vs Country for the sample
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
    print("Saving chart to:", os.path.abspath('static/health_chart.png'))
    return render_template("health-data.html", graph="health_chart.png")

@app.route("/wind-data")
def wind_data():
    # Read the file in chunks
    chunk_iter = pd.read_csv('wind_file2012.csv', chunksize=100000, low_memory=True)
    for chunk in chunk_iter:
        df = chunk.copy()
        break  # Only process the first chunk

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert WindSpeed to numeric (if not already)
    df['uwnd'] = pd.to_numeric(df['uwnd'], errors='coerce')

    # Example: Histogram of Wind Speed
    plt.figure(figsize=(10, 5))
    plt.hist(df['uwnd'].dropna(), bins=30, color='skyblue', edgecolor='black')
    plt.xlabel('Wind Speed (m/s)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Wind Speed (First Chunk)')
    plt.tight_layout()

    # Save the plot to static folder
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/wind_chart.png')
    plt.close()

    print("Saving chart to:", os.path.abspath('static/wind_chart.png'))
    return render_template("wind-data.html", graph="wind_chart.png")

if __name__ == "__main__":
    app.run(debug=True)
