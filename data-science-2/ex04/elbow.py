import matplotlib
matplotlib.use('Qt5Agg', force=True)
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import subprocess
import os

# Try Qt5Agg for Ubuntu
try:
    import matplotlib
    matplotlib.use('Qt5Agg')
    backend_found = True
    print("Using Qt5Agg backend")
except ImportError:
    backend_found = False
    print("Qt5Agg not available, will save and open image")

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

def calculate_elbow_point(x_values, y_values):
    """
    Calculate the elbow point using the maximum distance method
    """
    # Convert to numpy arrays for easier calculation
    x = np.array(x_values)
    y = np.array(y_values)
    
    # Calculate the line from first to last point
    line_vec = np.array([x[-1] - x[0], y[-1] - y[0]])
    line_vec_norm = line_vec / np.sqrt(np.sum(line_vec**2))
    
    # Calculate distance from each point to the line
    distances = []
    for i in range(len(x)):
        point_vec = np.array([x[i] - x[0], y[i] - y[0]])
        # Distance = |point_vec - proj_point_vec|
        proj_length = np.dot(point_vec, line_vec_norm)
        proj_point = proj_length * line_vec_norm
        distance = np.sqrt(np.sum((point_vec - proj_point)**2))
        distances.append(distance)
    
    # Return the k value with maximum distance (elbow point)
    elbow_index = np.argmax(distances)
    return x[elbow_index]

try:
    # 1. CALCULATE the values
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
    X = df[['purchase_frequency', 'total_spent']]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    K_range = range(2, 11)
    inertias = []
    
    print("Calculating Elbow Method...")
    print("k | Inertia")
    print("-" * 15)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        print(f"{k} | {kmeans.inertia_:.0f}")
    
    # 2. COPY into arrays with cast
    x_values = list(K_range)
    y_values = [int(inertia) for inertia in inertias]
    
    print(f"\nArrays created:")
    print(f"x_values = {x_values}")
    print(f"y_values = {y_values}")
    
    # 3. FIND the optimal number of clusters (elbow point)
    optimal_k = calculate_elbow_point(x_values, y_values)
    print(f"\nOptimal number of clusters detected: {optimal_k}")
    
    # 4. PLOT the arrays
    print("\nCreating plot...")
    
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.suptitle('ex04 - Elbow', fontsize=14, fontweight='bold')
    
    # Plot the elbow curve
    ax.plot(x_values, y_values, 'b-', linewidth=2, marker='o', markersize=8)
    
    # Add vertical line at optimal k
    ax.axvline(x=optimal_k, color='red', linestyle='--', linewidth=2, 
               label=f'Optimal k = {optimal_k}')
    
    # Highlight the elbow point
    optimal_index = x_values.index(optimal_k)
    ax.plot(optimal_k, y_values[optimal_index], 'ro', markersize=12, 
           markerfacecolor='red', markeredgecolor='darkred', markeredgewidth=2)
    
    ax.set_title('The Elbow Method', fontsize=12, fontweight='bold')
    ax.set_xlabel('Number of clusters', fontsize=11)
    ax.set_ylabel('Inertia', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Set x-axis ticks to show all k values
    ax.set_xticks(x_values)
    
    plt.tight_layout()
    
    # Try to show, fallback to save and open on Ubuntu
    if backend_found:
        try:
            plt.show()
        except:
            backend_found = False
    
    if not backend_found:
        # Save and open with default image viewer on Ubuntu
        filename = 'elbow_method.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved as {filename}")
        
        try:
            subprocess.run(['xdg-open', filename], check=True)
            print(f"Opening {filename} with default image viewer...")
        except subprocess.CalledProcessError:
            print(f"Could not auto-open. Run: xdg-open {filename}")
        except FileNotFoundError:
            print(f"xdg-open not found. Please open {filename} manually")
        
        plt.close()
    
    plt.close()

except Exception as e:
    print(f"Error during execution: {e}")
    
finally:
    # Close connection
    engine.dispose()