# Export all figures to images folder
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Create images directory if it doesn't exist
images_dir = 'images'
os.makedirs(images_dir, exist_ok=True)
print(f"📁 Created/verified images directory: {os.path.abspath(images_dir)}")

# Check current figures
fig_nums = plt.get_fignums()
print(f"🔍 Found {len(fig_nums)} existing figures")

# If no figures exist, regenerate key visualizations
if len(fig_nums) == 0:
    print("🔄 No figures found - regenerating key visualizations...")
    
    # Regenerate Department Performance Chart
    print("   📊 Generating Department Performance Visualization...")
    dept_viz_data = dept_performance_summary['dept_performance'].copy()
    dept_viz_data = dept_viz_data.sort_values('MAE', ascending=True)
    
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Top 15 best and worst
    top_15_best = dept_viz_data.head(15)
    top_15_worst = dept_viz_data.tail(15)
    comparison_data = pd.concat([top_15_best, top_15_worst])
    comparison_colors = ['#2E8B57'] * 15 + ['#8B0000'] * 15
    
    bars1 = ax1.barh(range(len(comparison_data)), comparison_data['MAE'], color=comparison_colors)
    ax1.set_yticks(range(len(comparison_data)))
    ax1.set_yticklabels([f"Dept {d}" for d in comparison_data.index])
    ax1.set_xlabel('Mean Absolute Error (MAE)')
    ax1.set_title('Department Performance: Best vs Worst')
    ax1.grid(axis='x', alpha=0.3)
    
    # Performance distribution
    ax2.hist(dept_viz_data['MAE'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Mean Absolute Error (MAE)')
    ax2.set_ylabel('Number of Departments')
    ax2.set_title('Distribution of Department Performance')
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'department_performance_comparison.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("   ✅ Department Performance chart saved")
    
    # Regenerate Seasonal Analysis (simplified version)
    print("   📊 Generating Seasonal Analysis Visualization...")
    fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Seasonal heatmap
    seasonal_pivot_clean = seasonal_pivot.fillna(0)
    im1 = ax1.imshow(seasonal_pivot_clean.values, cmap='RdYlBu_r', aspect='auto')
    ax1.set_xticks(range(len(seasonal_pivot_clean.columns)))
    ax1.set_xticklabels(seasonal_pivot_clean.columns)
    ax1.set_yticks(range(len(seasonal_pivot_clean.index)))
    ax1.set_yticklabels([f"Dept {d}" for d in seasonal_pivot_clean.index])
    ax1.set_title('Seasonal Performance Heatmap')
    
    # Add colorbar to show MAE scale
    plt.colorbar(im1, ax=ax1, label='MAE')
    
    # Add text annotations showing values in each cell
    for i in range(len(seasonal_pivot_clean.index)):
        for j in range(len(seasonal_pivot_clean.columns)):
            value = seasonal_pivot_clean.iloc[i, j]
            # Format value to 1 decimal place, show only if not zero
            if value != 0:
                ax1.text(j, i, f'{value:.1f}', ha='center', va='center', 
                        color='white', fontsize=12, fontweight='bold')
    
    # 2. Simple department MAE bar chart
    top_depts = dept_viz_data.head(10)
    bars = ax2.bar(range(len(top_depts)), top_depts['MAE'], 
                  color='lightcoral', alpha=0.7)
    ax2.set_xticks(range(len(top_depts)))
    ax2.set_xticklabels([f"Dept {d}" for d in top_depts.index], rotation=45)
    ax2.set_ylabel('MAE')
    ax2.set_title('Top 10 Best Performing Departments')
    
    # 3. Performance matrix (simplified and cleaner)
    try:
        if 'performance_matrix' in locals() and performance_matrix is not None:
            # Create a simplified matrix with key metrics for top/bottom departments
            dept_viz_data_sorted = dept_viz_data.sort_values('MAE')
            
            # Select top 5 best and top 5 worst for cleaner visualization
            top_5_best = dept_viz_data_sorted.head(5)
            top_5_worst = dept_viz_data_sorted.tail(5)
            matrix_depts = pd.concat([top_5_best, top_5_worst])
            
            # Create simplified performance matrix with key metrics only
            if len(performance_matrix.columns) > 10:
                # If too many metrics, select key ones (every 5th column or specific metrics)
                key_metrics = performance_matrix.columns[::max(1, len(performance_matrix.columns)//8)]
                simplified_matrix = performance_matrix.loc[matrix_depts.index, key_metrics]
            else:
                simplified_matrix = performance_matrix.loc[matrix_depts.index]
            
            # Normalize for better color visualization
            from sklearn.preprocessing import StandardScaler
            scaler_temp = StandardScaler()
            normalized_data = scaler_temp.fit_transform(simplified_matrix)
            
            im2 = ax3.imshow(normalized_data, cmap='RdYlGn_r', aspect='auto')
            ax3.set_title('Department Performance Matrix\\n(Top 5 Best vs Worst)')
            ax3.set_xlabel('Key Metrics')
            ax3.set_ylabel('Departments')
            
            # Set cleaner labels
            ax3.set_xticks(range(len(simplified_matrix.columns)))
            ax3.set_xticklabels([str(col)[:10] for col in simplified_matrix.columns], rotation=45, fontsize=8)
            ax3.set_yticks(range(len(simplified_matrix.index)))
            ax3.set_yticklabels([f"Dept {idx}" for idx in simplified_matrix.index], fontsize=9)
            
            # Add colorbar
            plt.colorbar(im2, ax=ax3, label='Normalized Performance')
            
            # Add text annotations showing values in each cell
            for i in range(len(simplified_matrix.index)):
                for j in range(len(simplified_matrix.columns)):
                    # Show the original (non-normalized) values for clarity
                    value = simplified_matrix.iloc[i, j]
                    ax3.text(j, i, f'{value:.1f}', ha='center', va='center', 
                            color='white', fontsize=11, fontweight='bold')
        else:
            ax3.text(0.5, 0.5, 'Performance Matrix\\nNot Available', 
                    ha='center', va='center', transform=ax3.transAxes, fontsize=14)
            ax3.set_title('Performance Matrix')
    except Exception as e:
        # Fallback: Create a simple performance comparison
        try:
            dept_viz_data_sorted = dept_viz_data.sort_values('MAE')
            top_5_best = dept_viz_data_sorted.head(5)
            top_5_worst = dept_viz_data_sorted.tail(5)
            
            # Simple matrix showing MAE values
            matrix_data = np.array([top_5_best['MAE'].values, top_5_worst['MAE'].values])
            
            im2 = ax3.imshow(matrix_data, cmap='RdYlGn_r', aspect='auto')
            ax3.set_title('Department Performance Comparison\\n(Best vs Worst MAE)')
            ax3.set_xlabel('Department Rank')
            ax3.set_ylabel('Performance Group')
            ax3.set_yticks([0, 1])
            ax3.set_yticklabels(['Top 5 Best', 'Top 5 Worst'])
            ax3.set_xticks(range(5))
            ax3.set_xticklabels(['1st', '2nd', '3rd', '4th', '5th'])
            
            plt.colorbar(im2, ax=ax3, label='MAE')
            
            # Add text annotations showing MAE values in each cell
            for i in range(matrix_data.shape[0]):
                for j in range(matrix_data.shape[1]):
                    value = matrix_data[i, j]
                    ax3.text(j, i, f'{value:.1f}', ha='center', va='center', 
                            color='white', fontsize=12, fontweight='bold')
        except:
            ax3.text(0.5, 0.5, 'Performance Matrix\\nError Loading Data', 
                    ha='center', va='center', transform=ax3.transAxes, fontsize=14)
            ax3.set_title('Performance Matrix')
    
    # 4. Strategic departments (if available)
    try:
        # Use revenue_weighted_analysis for more comprehensive strategic view
        if 'revenue_weighted_analysis' in globals() and not revenue_weighted_analysis.empty:
            # Select top departments by revenue impact for strategic analysis
            strategic_viz_data = revenue_weighted_analysis.head(15).copy()
            
            # Create meaningful strategic analysis visualization
            scatter = ax4.scatter(strategic_viz_data['MAE'], strategic_viz_data['Revenue_Share'] * 100, 
                                s=strategic_viz_data['Sample_Count']/20, 
                                alpha=0.7, 
                                c=strategic_viz_data['Revenue_Share'] * 100, 
                                cmap='viridis',
                                edgecolors='black')
            ax4.set_xlabel('Mean Absolute Error (MAE)')
            ax4.set_ylabel('Revenue Share (%)')
            ax4.set_title('Strategic Department Analysis\\n(Top 15 by Revenue Impact)')
            ax4.grid(True, alpha=0.3)
            
            # Add non-overlapping department labels using smart positioning
            try:
                from adjustText import adjust_text
                texts = []
                for idx, row in strategic_viz_data.iterrows():
                    text = ax4.text(row['MAE'], row['Revenue_Share'] * 100, f'Dept {idx}',
                                   fontsize=8, weight='bold', ha='center',
                                   bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8, edgecolor='gray'))
                    texts.append(text)
                
                # Automatically adjust text positions to prevent overlap
                adjust_text(texts, ax=ax4, arrowprops=dict(arrowstyle='->', color='gray', alpha=0.6, lw=0.5))
                
            except ImportError:
                # Fallback: Use varied offset positions to reduce overlap
                import numpy as np
                offsets = [(5, 5), (-5, 5), (5, -5), (-5, -5), (10, 0), (-10, 0), (0, 10), (0, -10),
                          (8, 8), (-8, 8), (8, -8), (-8, -8), (12, 3), (-12, 3), (3, 12)]
                
                for i, (idx, row) in enumerate(strategic_viz_data.iterrows()):
                    offset = offsets[i % len(offsets)]
                    ax4.annotate(f'Dept {idx}', 
                               (row['MAE'], row['Revenue_Share'] * 100),
                               xytext=offset, textcoords='offset points',
                               fontsize=8, alpha=0.9, weight='bold',
                               bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7),
                               arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5, lw=0.5))
            
            # Add colorbar
            plt.colorbar(scatter, ax=ax4, label='Revenue %')
            
        elif 'strategic_assets' in globals() and not strategic_assets.empty:
            # Fallback to strategic_assets if available
            scatter = ax4.scatter(strategic_assets['MAE'], strategic_assets['Revenue_Share'] * 100, 
                                s=strategic_assets['Sample_Count']/50, 
                                alpha=0.7, c='purple', edgecolors='black')
            ax4.set_xlabel('Mean Absolute Error (MAE)')
            ax4.set_ylabel('Revenue Share (%)')
            ax4.set_title('Strategic Department Analysis\\n(Strategic Assets Only)')
            ax4.grid(True, alpha=0.3)
            
            # Add non-overlapping labels for strategic assets
            try:
                from adjustText import adjust_text
                texts = []
                for idx, row in strategic_assets.iterrows():
                    text = ax4.text(row['MAE'], row['Revenue_Share'] * 100, f'Dept {idx}',
                                   fontsize=9, weight='bold', ha='center',
                                   bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
                    texts.append(text)
                
                adjust_text(texts, ax=ax4, arrowprops=dict(arrowstyle='->', color='gray', alpha=0.6, lw=0.5))
                
            except ImportError:
                # Fallback with varied offsets
                offsets = [(5, 5), (-5, 5), (5, -5), (-5, -5), (10, 0), (-10, 0)]
                for i, (idx, row) in enumerate(strategic_assets.iterrows()):
                    offset = offsets[i % len(offsets)]
                    ax4.annotate(f'Dept {idx}', 
                               (row['MAE'], row['Revenue_Share'] * 100),
                               xytext=offset, textcoords='offset points',
                               fontsize=9, alpha=0.8, weight='bold',
                               arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5, lw=0.5))
        else:
            # Create sample strategic analysis if data not available
            sample_mae = [50, 75, 100, 125, 150, 200, 80, 90, 110, 140, 160, 180]
            sample_revenue = [8.5, 6.2, 4.8, 3.5, 2.1, 1.8, 5.5, 4.2, 3.8, 2.8, 2.3, 1.9]
            sample_depts = [92, 95, 38, 40, 72, 90, 81, 97, 85, 99, 14, 13]
            sample_sizes = [800, 600, 500, 400, 300, 200, 450, 350, 380, 320, 280, 250]
            
            scatter = ax4.scatter(sample_mae, sample_revenue, 
                                s=sample_sizes, 
                                alpha=0.6, 
                                c=sample_revenue,
                                cmap='viridis',
                                edgecolors='black')
            ax4.set_xlabel('Mean Absolute Error (MAE)')
            ax4.set_ylabel('Revenue Percentage (%)')
            ax4.set_title('Strategic Department Analysis\\n(Sample Data - 12 Departments)')
            ax4.grid(True, alpha=0.3)
            
            # Add non-overlapping labels for sample data
            try:
                from adjustText import adjust_text
                texts = []
                for i, dept in enumerate(sample_depts):
                    text = ax4.text(sample_mae[i], sample_revenue[i], f'Dept {dept}',
                                   fontsize=8, weight='bold', ha='center',
                                   bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8, edgecolor='gray'))
                    texts.append(text)
                
                adjust_text(texts, ax=ax4, arrowprops=dict(arrowstyle='->', color='gray', alpha=0.6, lw=0.5))
                
            except ImportError:
                # Fallback with varied offsets to minimize overlap
                offsets = [(5, 5), (-5, 5), (5, -5), (-5, -5), (10, 0), (-10, 0), (0, 10), (0, -10),
                          (8, 8), (-8, 8), (8, -8), (-8, -8)]
                
                for i, dept in enumerate(sample_depts):
                    offset = offsets[i % len(offsets)]
                    ax4.annotate(f'Dept {dept}', 
                               (sample_mae[i], sample_revenue[i]),
                               xytext=offset, textcoords='offset points',
                               fontsize=8, alpha=0.8, weight='bold',
                               bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.7),
                               arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5, lw=0.5))
            
            plt.colorbar(scatter, ax=ax4, label='Revenue %')
            
    except Exception as e:
        print(f"Strategic analysis error: {e}")
        ax4.text(0.5, 0.5, f'Strategic Analysis\\nError: {str(e)}', 
                ha='center', va='center', transform=ax4.transAxes, fontsize=12)
        ax4.set_title('Strategic Department Analysis')
    
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, 'comprehensive_analysis_dashboard.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    print("   ✅ Comprehensive dashboard saved")

# Now export all figures
fig_nums = plt.get_fignums()
print(f"\\n📊 Exporting {len(fig_nums)} figures...")

# Define descriptive names
figure_names = {
    1: "department_performance_comparison",
    2: "comprehensive_analysis_dashboard", 
    3: "seasonal_performance_analysis",
    4: "strategic_department_visualization",
    5: "additional_analysis"
}

exported_count = 0
for fig_num in fig_nums:
    try:
        fig = plt.figure(fig_num)
        
        # Generate filename
        if fig_num in figure_names:
            filename = f"{figure_names[fig_num]}.png"
        else:
            filename = f"figure_{fig_num}.png"
        
        filepath = os.path.join(images_dir, filename)
        
        # Save with high quality
        fig.savefig(filepath, 
                   dpi=300, 
                   bbox_inches='tight', 
                   facecolor='white', 
                   edgecolor='none',
                   format='png')
        
        print(f"✅ Exported: {filename}")
        exported_count += 1
        
    except Exception as e:
        print(f"❌ Error exporting figure {fig_num}: {str(e)}")

# Create export log
timestamp_file = os.path.join(images_dir, 'export_log.txt')
with open(timestamp_file, 'w') as f:
    f.write(f"Walmart Sales Forecast - Image Export Log\\n")
    f.write(f"=========================================\\n\\n")
    f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
    f.write(f"Source Notebook: department-performance-analysis.ipynb\\n")
    f.write(f"Total Figures Exported: {exported_count}\\n\\n")
    f.write("Exported Files:\\n")
    for fig_num in fig_nums:
        if fig_num in figure_names:
            filename = f"{figure_names[fig_num]}.png"
        else:
            filename = f"figure_{fig_num}.png"
        f.write(f"- {filename}\\n")

print(f"\\n🎉 Export Complete!")
print(f"📊 Total figures exported: {exported_count}")
print(f"📁 Location: {os.path.abspath(images_dir)}")
print(f"📝 Export log: export_log.txt")