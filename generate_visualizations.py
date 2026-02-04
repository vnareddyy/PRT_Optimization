"""
PRT Survey Data Analysis - Visualizations
Generates charts and graphs from the survey analysis results
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import os

# Create output directory
os.makedirs('/Users/vinaynareddy/Documents/ds_practicum/visualizations', exist_ok=True)

# Load data
routes_df = pd.read_csv('/Users/vinaynareddy/Documents/ds_practicum/data/processed/routes_mentioned.csv')
actions_df = pd.read_csv('/Users/vinaynareddy/Documents/ds_practicum/data/processed/action_types.csv')
areas_df = pd.read_csv('/Users/vinaynareddy/Documents/ds_practicum/data/processed/geographic_areas.csv')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Color schemes
route_colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, 15))
action_colors = plt.cm.Set2(np.linspace(0, 1, 8))
area_colors = plt.cm.Blues(np.linspace(0.3, 0.9, 15))

# ============================================
# 1. ROUTE FREQUENCY BAR CHART
# ============================================
fig, ax = plt.subplots(figsize=(14, 8))

top_routes = routes_df.head(15)
bars = ax.barh(range(len(top_routes)), top_routes['Count'], color=route_colors)
ax.set_yticks(range(len(top_routes)))
ax.set_yticklabels([f"Route {r}" for r in top_routes['Route']])
ax.invert_yaxis()
ax.set_xlabel('Number of Mentions', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Bus Routes by Survey Mentions\nPRT Network Redesign Feedback', fontsize=14, fontweight='bold')

# Add value labels
for i, (count, bar) in enumerate(zip(top_routes['Count'], bars)):
    ax.text(count + 3, i, str(count), va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/vinaynareddy/Documents/ds_practicum/visualizations/route_frequency.png', dpi=150, bbox_inches='tight')
print("✓ Saved: route_frequency.png")
plt.close()

# ============================================
# 2. ACTION TYPE PIE CHART
# ============================================
fig, ax = plt.subplots(figsize=(10, 10))

# Filter out zero counts
actions_df_filtered = actions_df[actions_df['Count'] > 0].sort_values('Count', ascending=False)
labels = actions_df_filtered['Action_Type'].str.replace('_', '\n')
sizes = actions_df_filtered['Count']
explode = [0.05] * len(labels)

wedges, texts, autotexts = ax.pie(
    sizes, 
    labels=labels,
    autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(sizes))})',
    colors=action_colors[:len(labels)],
    explode=explode,
    shadow=True,
    startangle=90
)

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')

ax.set_title('Distribution of Rider Request Types\nSurvey Response Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/vinaynareddy/Documents/ds_practicum/visualizations/action_distribution.png', dpi=150, bbox_inches='tight')
print("✓ Saved: action_distribution.png")
plt.close()

# ============================================
# 3. GEOGRAPHIC AREAS BAR CHART
# ============================================
fig, ax = plt.subplots(figsize=(12, 8))

top_areas = areas_df.head(12)
bars = ax.barh(range(len(top_areas)), top_areas['Count'], color=area_colors)
ax.set_yticks(range(len(top_areas)))
ax.set_yticklabels([a.title() for a in top_areas['Area']])
ax.invert_yaxis()
ax.set_xlabel('Number of Mentions', fontsize=12, fontweight='bold')
ax.set_title('Most Mentioned Geographic Areas\nPittsburgh Neighborhoods in Survey Responses', fontsize=14, fontweight='bold')

for i, (count, bar) in enumerate(zip(top_areas['Count'], bars)):
    ax.text(count + 3, i, str(count), va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/vinaynareddy/Documents/ds_practicum/visualizations/geographic_distribution.png', dpi=150, bbox_inches='tight')
print("✓ Saved: geographic_distribution.png")
plt.close()

# ============================================
# 4. PRIORITY MATRIX (Route vs Priority)
# ============================================
fig, ax = plt.subplots(figsize=(12, 10))

# Define priority thresholds
routes_data = routes_df.head(25).to_dict('records')
high_priority = [(r['Route'], r['Count']) for r in routes_data if r['Count'] >= 150]
medium_priority = [(r['Route'], r['Count']) for r in routes_data if 100 <= r['Count'] < 150]
low_priority = [(r['Route'], r['Count']) for r in routes_data if r['Count'] < 100]

y_pos = 0
for routes, color, label in [
    (high_priority, 'red', '🔴 HIGH PRIORITY (≥150 mentions)'),
    (medium_priority, 'orange', '🟠 MEDIUM PRIORITY (100-149 mentions)'),
    (low_priority, 'green', '🟢 LOW PRIORITY (<100 mentions)')
]:
    for route, count in routes:
        ax.scatter(count, y_pos, c=color, s=150, alpha=0.7, edgecolors='black', linewidth=1)
        ax.text(count + 5, y_pos, f"Route {route}", va='center', fontsize=9)
        y_pos += 1

ax.set_xlabel('Number of Mentions', fontsize=12, fontweight='bold')
ax.set_ylabel('Route Priority', fontsize=12, fontweight='bold')
ax.set_title('Route Priority Matrix\nBased on Survey Response Frequency', fontsize=14, fontweight='bold')
ax.legend(loc='lower right', fontsize=10)
ax.set_xlim(0, 300)
plt.tight_layout()
plt.savefig('/Users/vinaynareddy/Documents/ds_practicum/visualizations/priority_matrix.png', dpi=150, bbox_inches='tight')
print("✓ Saved: priority_matrix.png")
plt.close()

# ============================================
# 5. SUMMARY DASHBOARD
# ============================================
fig = plt.figure(figsize=(20, 16))
fig.suptitle('PRT Survey Analysis Dashboard\nPittsburgh Regional Transit Network Redesign Feedback', 
             fontsize=20, fontweight='bold', y=0.98)

# Subplot 1: Route Frequency (top left)
ax1 = fig.add_subplot(2, 2, 1)
top10 = routes_df.head(10)
colors1 = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, 10))
ax1.barh(range(len(top10)), top10['Count'], color=colors1)
ax1.set_yticks(range(len(top10)))
ax1.set_yticklabels([f"Route {r}" for r in top10['Route']])
ax1.invert_yaxis()
ax1.set_xlabel('Mentions')
ax1.set_title('Top 10 Routes by Mentions', fontweight='bold')

# Subplot 2: Action Distribution (top right)
ax2 = fig.add_subplot(2, 2, 2)
actions_filtered = actions_df[actions_df['Count'] > 0].sort_values('Count', ascending=False)
ax2.pie(actions_filtered['Count'], 
         labels=[a.replace('_', '\n') for a in actions_filtered['Action_Type']], 
         autopct='%1.1f%%',
         colors=action_colors[:len(actions_filtered)],
         startangle=90)
ax2.set_title('Request Type Distribution', fontweight='bold')

# Subplot 3: Geographic Areas (bottom left)
ax3 = fig.add_subplot(2, 2, 3)
top8 = areas_df.head(8)
ax3.barh(range(len(top8)), top8['Count'], color='steelblue')
ax3.set_yticks(range(len(top8)))
ax3.set_yticklabels([a.title() for a in top8['Area']])
ax3.invert_yaxis()
ax3.set_xlabel('Mentions')
ax3.set_title('Top Geographic Areas', fontweight='bold')

# Subplot 4: Summary Statistics (bottom right)
ax4 = fig.add_subplot(2, 2, 4)
ax4.axis('off')

summary_text = f"""
╔══════════════════════════════════════════╗
║     PRT SURVEY ANALYSIS SUMMARY          ║
╠══════════════════════════════════════════╣
║                                          ║
║  Total Survey Responses:  1,736          ║
║                                          ║
║  ROUTE ANALYSIS                          ║
║  • Unique Routes Found: 178              ║
║  • High Priority Routes: 2               ║
║  • (54, 28X with 200+ mentions)         ║
║                                          ║
║  ACTION TYPES                            ║
║  • Increase Frequency: 501 (51%)        ║
║  • Improve Coverage: 165 (17%)           ║
║  • Add Service: 137 (14%)                ║
║                                          ║
║  TOP DESTINATIONS                        ║
║  • Downtown: 317 mentions               ║
║  • Oakland: 279 mentions                 ║
║                                          ║
║  KEY FINDINGS                            ║
║  • Route 54 needs attention              ║
║  • Frequency is #1 concern              ║
║  • South Hills-Oakland gap              ║
║                                          ║
╚══════════════════════════════════════════╝
"""

ax4.text(0.1, 0.95, summary_text, transform=ax4.transAxes, 
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('/Users/vinaynareddy/Documents/ds_practicum/visualizations/summary_dashboard.png', dpi=150, bbox_inches='tight')
print("✓ Saved: summary_dashboard.png")
plt.close()

# ============================================
# 6. HORIZONTAL STACKED BAR - ROUTES BY CATEGORY
# ============================================
fig, ax = plt.subplots(figsize=(14, 10))

# Categorize routes
top15 = routes_df.head(15)
categories = []
for _, row in top15.iterrows():
    if row['Count'] >= 200:
        categories.append('Critical')
    elif row['Count'] >= 150:
        categories.append('High')
    elif row['Count'] >= 100:
        categories.append('Medium')
    else:
        categories.append('Standard')

colors_map = {'Critical': 'darkred', 'High': 'orangered', 'Medium': 'orange', 'Standard': 'steelblue'}
bar_colors = [colors_map[c] for c in categories]

bars = ax.barh(range(len(top15)), top15['Count'], color=bar_colors)
ax.set_yticks(range(len(top15)))
ax.set_yticklabels([f"Route {r}" for r in top15['Route']])
ax.invert_yaxis()
ax.set_xlabel('Number of Mentions', fontsize=12, fontweight='bold')
ax.set_title('Route Priority Classification\nPRT Network Redesign Survey', fontsize=14, fontweight='bold')

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='darkred', label='Critical (≥200)'),
                  Patch(facecolor='orangered', label='High (150-199)'),
                  Patch(facecolor='orange', label='Medium (100-149)'),
                  Patch(facecolor='steelblue', label='Standard (<100)')]
ax.legend(handles=legend_elements, loc='lower right')

# Add value labels
for i, (count, bar) in enumerate(zip(top15['Count'], bars)):
    ax.text(count + 3, i, str(count), va='center', fontsize=10)

plt.tight_layout()
plt.savefig('/Users/vinaynareddy/Documents/ds_practicum/visualizations/route_priority.png', dpi=150, bbox_inches='tight')
print("✓ Saved: route_priority.png")
plt.close()

# ============================================
# PRINT SUMMARY
# ============================================
print("\n" + "="*60)
print("VISUALIZATION GENERATION COMPLETE")
print("="*60)
print(f"\n📊 Generated 6 visualization files:")
print("   1. route_frequency.png")
print("   2. action_distribution.png")
print("   3. geographic_distribution.png")
print("   4. priority_matrix.png")
print("   5. summary_dashboard.png")
print("   6. route_priority.png")
print(f"\n📁 Output directory:")
print("   /Users/vinaynareddy/Documents/ds_practicum/visualizations/")
print("="*60)

