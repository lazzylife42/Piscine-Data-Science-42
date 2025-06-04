import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

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

# SQL query to retrieve event_type distribution
query = """
SELECT event_type, COUNT(*) as count
FROM customers 
GROUP BY event_type
ORDER BY count DESC;
"""

try:
	# Retrieve data
	df = pd.read_sql(query, engine)
	print("Data retrieved:")
	print(df)
	
	# Configure Seaborn style
	sns.set_style("whitegrid")
	plt.figure(figsize=(10, 8))
	
	# Create pie chart with matplotlib
	colors = sns.color_palette("husl", len(df))
	
	plt.pie(df['count'], 
			labels=df['event_type'], 
			autopct='%1.1f%%',
			startangle=90,
			colors=colors,
			explode=None)
	
	plt.title('Distribution of Event Types', 
			  fontsize=16, fontweight='bold', pad=20)
	
	
	# Display the chart
	plt.tight_layout()
	plt.show()
	
	# Also display a text summary
	print("\nDistribution summary:")
	total = df['count'].sum()
	for _, row in df.iterrows():
		percentage = (row['count'] / total) * 100
		print(f"{row['event_type']}: {row['count']} ({percentage:.1f}%)")

except Exception as e:
	print(f"Error during execution: {e}")

finally:
	# Close connection
	engine.dispose()