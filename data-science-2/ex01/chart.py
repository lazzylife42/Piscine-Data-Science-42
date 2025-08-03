import matplotlib
matplotlib.use('Qt5Agg', force=True)
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.dates as mdates
import numpy as np

# Database configuration
DATABASE_CONFIG = {
	'host': 'localhost',
	'port': '5432',
	'database': 'piscineds',
	'username': 'smonte',
	'password': 'mysecretpassword'
}
DATABASE_URL = f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?gssencmode=disable"

# Create connection
engine = create_engine(DATABASE_URL)

try:
	# Query 1: Daily purchases count
	query1 = """
	SELECT DATE(event_time) as date, COUNT(*) as number_of_purchases
	FROM customers 
	WHERE event_type = 'purchase'
	  AND event_time >= '2022-10-01' 
	  AND event_time <= '2023-02-28'
	GROUP BY DATE(event_time)
	ORDER BY date;
	"""
	
	# Query 2: Monthly total sales
	query2 = """
	SELECT 
		EXTRACT(YEAR FROM event_time) as year,
		EXTRACT(MONTH FROM event_time) as month,
		SUM(price) as total_sales
	FROM customers 
	WHERE event_type = 'purchase'
	  AND event_time >= '2022-10-01' 
	  AND event_time <= '2023-02-28'
	GROUP BY EXTRACT(YEAR FROM event_time), EXTRACT(MONTH FROM event_time)
	ORDER BY year, month;
	"""
	
	# Query 3: Daily average spending per customer
	query3 = """
	SELECT 
		DATE(event_time) as date, 
		AVG(price) as average_spend
	FROM customers 
	WHERE event_type = 'purchase'
	  AND event_time >= '2022-10-01' 
	  AND event_time <= '2023-02-28'
	GROUP BY DATE(event_time)
	ORDER BY date;
	"""
	
	# Retrieve data
	df1 = pd.read_sql(query1, engine)
	df2 = pd.read_sql(query2, engine)
	df3 = pd.read_sql(query3, engine)
	
	# Convert dates
	df1['date'] = pd.to_datetime(df1['date'])
	df3['date'] = pd.to_datetime(df3['date'])
	
	# Create proper dates for monthly data (middle of each month)
	df2['date'] = pd.to_datetime(df2[['year', 'month']].assign(day=15))
	
	# Configure the multiplot with shared x-axis
	sns.set_style("whitegrid")
	fig, axes = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
	fig.suptitle('ex01 - initial data exploration', fontsize=16, fontweight='bold')
	
	# Plot 1: Number of purchases over time (line plot)
	axes[0].plot(df1['date'], df1['number_of_purchases'], 
				 marker='None', linestyle='-', linewidth=1.5, 
				 markersize=2, color='steelblue', alpha=0.8)
	axes[0].set_ylabel('Number of purchases', fontsize=10)
	axes[0].grid(True, alpha=0.3)
	
	# Plot 2: Total sales by month (bar chart) - aligned with dates
	bar_width = 20
	axes[1].bar(df2['date'], df2['total_sales'] / 1000000, 
				width=bar_width, color='lightblue', alpha=0.7, 
				edgecolor='white', align='center')
	axes[1].set_ylabel('total sales in million of ₳', fontsize=10)
	axes[1].grid(True, alpha=0.3, axis='y')
	
	# Plot 3: Average spending per customer (area plot)
	axes[2].fill_between(df3['date'], df3['average_spend'], 
						 alpha=0.6, color='lightblue', 
						 edgecolor='steelblue', linewidth=1)
	axes[2].set_ylabel('average spend/customers in ₳', fontsize=10)
	axes[2].grid(True, alpha=0.3)
	
	# Configure x-axis for all plots
	for ax in axes:
		ax.xaxis.set_major_locator(mdates.MonthLocator())
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
		ax.set_xlim(pd.to_datetime('2022-10-01'), pd.to_datetime('2023-02-28'))
	
	# Only show x-axis labels on the bottom plot
	axes[0].set_xticklabels([])
	
	# For 2nd graph month labels
	month_positions = [pd.to_datetime(f'2022-{m}-15') for m in [10, 11, 12]] + \
					[pd.to_datetime(f'2023-{m}-15') for m in [1, 2]]
	axes[1].set_xticks(month_positions)
	axes[1].set_xticklabels(['Oct', 'Nov','Dec', 'Jan', 'Feb'])
	
	# Adjust layout
	plt.tight_layout()
	plt.subplots_adjust(top=0.93)
	plt.show()
	
	print("Multiplot created successfully!")
	
except Exception as e:
	print(f"Error during execution: {e}")
finally:
	# Close connection
	engine.dispose()