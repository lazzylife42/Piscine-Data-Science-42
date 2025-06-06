import matplotlib
matplotlib.use('Qt5Agg', force=True)
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import subprocess

# Database configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'piscineds',
    'username': 'smonte',
    'password': 'mysecretpassword'
}

DATABASE_URL = f"postgresql://{DATABASE_CONFIG['username']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}?gssencmode=disable"
engine = create_engine(DATABASE_URL)

# Try Qt5Agg for Ubuntu
try:
    import matplotlib
    matplotlib.use('Qt5Agg')
    backend_found = True
    print("Using Qt5Agg backend")
except ImportError:
    backend_found = False
    print("Qt5Agg not available, will save and open images")

def save_and_open_plot(filename):
    """Save plot and try to open it on Ubuntu"""
    if not backend_found:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved as {filename}")
        try:
            subprocess.run(['xdg-open', filename], check=True)
            print(f"Opening {filename}...")
        except:
            print(f"Could not auto-open. Run: xdg-open {filename}")
        plt.close()

try:
    print("Fetching customer data...")
    
    # Get customer purchase data
    query = """
    SELECT 
        user_id,
        COUNT(*) as purchase_frequency,
        SUM(price) as total_spent
    FROM customers 
    WHERE event_type = 'purchase'
    GROUP BY user_id
    HAVING SUM(price) >= 0;
    """
    
    df = pd.read_sql(query, engine)
    print(f"Loaded {len(df)} customers")
    
    # Prepare data for clustering
    X = df[['purchase_frequency', 'total_spent']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-means clustering with 5 clusters
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    df['cluster'] = clusters
    
    # Analyze each cluster to assign logical names
    cluster_analysis = {}
    for cluster_id in range(5):
        cluster_data = df[df['cluster'] == cluster_id]
        avg_freq = cluster_data['purchase_frequency'].mean()
        avg_spent = cluster_data['total_spent'].mean()
        cluster_analysis[cluster_id] = {
            'avg_freq': avg_freq,
            'avg_spent': avg_spent,
            'count': len(cluster_data)
        }
    
    # Assign logical names based on actual cluster characteristics
    sorted_clusters = sorted(cluster_analysis.items(), 
                           key=lambda x: (x[1]['avg_freq'], x[1]['avg_spent']))
    
    cluster_names = {}
    cluster_names[sorted_clusters[0][0]] = 'Inactive'           # Lowest freq + spending
    cluster_names[sorted_clusters[1][0]] = 'New customers'      # Low-medium 
    cluster_names[sorted_clusters[2][0]] = 'Occasional customers' # Medium
    cluster_names[sorted_clusters[3][0]] = 'Loyal customers'    # High freq, medium spending
    cluster_names[sorted_clusters[4][0]] = 'VIP customers'      # Highest freq + spending
    
    df['customer_category'] = df['cluster'].map(cluster_names)
    
    # Print category distribution with descriptions
    print("\nCustomer Category Distribution:")
    category_counts = df['customer_category'].value_counts()
    for cat, count in category_counts.items():
        print(f"{cat}: {count}")
    
    # Print detailed descriptions
    print("\n" + "="*50)
    print("CATEGORY DESCRIPTIONS:")
    print("="*50)
    for category in category_counts.index:
        cat_data = df[df['customer_category'] == category]
        avg_freq = cat_data['purchase_frequency'].mean()
        avg_spent = cat_data['total_spent'].mean()
        print(f"\n{category}:")
        print(f"  → Count: {len(cat_data)} customers")
        print(f"  → Avg frequency: {avg_freq:.1f} purchases")
        print(f"  → Avg spending: {avg_spent:.1f}₳ per customer")
        print(f"  → Total revenue: {cat_data['total_spent'].sum():.0f}₳")
    
    # GRAPH 1: Horizontal bar chart
    plt.figure(figsize=(12, 6))
    
    category_colors = {
        'Loyal customers': '#D2B48C',     
        'New customers': '#87CEEB',       
        'Inactive': '#90EE90',            
        'VIP customers': '#FFB6C1',       
        'Occasional customers': '#DDA0DD' 
    }
    
    categories = category_counts.index[::-1]  # Reverse for descending order
    counts = category_counts.values[::-1]
    colors = [category_colors[cat] for cat in categories]
    
    bars = plt.barh(categories, counts, color=colors)
    
    for i, (bar, count) in enumerate(zip(bars, counts)):
        plt.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2, 
                str(count), ha='left', va='center', fontweight='bold')
    
    plt.xlabel('number of customers')
    plt.title('Customer Categories Distribution')
    plt.xlim(0, max(counts) * 1.15)
    plt.tight_layout()
    
    if backend_found:
        try:
            plt.show()
        except:
            save_and_open_plot('customer_categories.png')
    else:
        save_and_open_plot('customer_categories.png')
    
    # GRAPH 2: Scatter plot of clusters in 2D
    plt.figure(figsize=(10, 8))
    
    cluster_colors = {
        'Loyal customers': '#D2B48C',     
        'New customers': '#87CEEB',       
        'Inactive': '#90EE90',            
        'VIP customers': '#FFB6C1',       
        'Occasional customers': '#DDA0DD' 
    }
    
    for category in df['customer_category'].unique():
        cat_data = df[df['customer_category'] == category]
        plt.scatter(cat_data['purchase_frequency'], 
                   cat_data['total_spent'],
                   c=cluster_colors[category],
                   label=category,
                   alpha=0.6,
                   s=20)
    
    centroids_original = scaler.inverse_transform(kmeans.cluster_centers_)
    plt.scatter(centroids_original[:, 0], centroids_original[:, 1], 
               c='yellow', marker='o', s=200, edgecolors='black', linewidth=2,
               label='Centroids')
    
    plt.xlabel('Purchase Frequency')
    plt.ylabel('Total Spent (₳)') 
    plt.title('Clusters of customers')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Show full data range to see all clusters
    plt.xlim(0, df['purchase_frequency'].max() * 1.05)
    plt.ylim(0, df['total_spent'].max() * 1.05)
    
    plt.tight_layout()
    
    if backend_found:
        try:
            plt.show()
        except:
            save_and_open_plot('customer_clusters.png')
    else:
        save_and_open_plot('customer_clusters.png')

except Exception as e:
    print(f"Error during execution: {e}")
finally:
    engine.dispose()