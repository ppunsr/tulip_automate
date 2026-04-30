import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np
import json
import sys
import os
import argparse

# Determine the absolute path to the workspace root and the font file
font_path = os.path.abspath('fonts/THSarabunNew.ttf')

# Register the font with matplotlib
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'TH Sarabun New'
    # Increase default font size for better readability
    plt.rcParams['font.size'] = 24
else:
    print(f"Warning: Thai font not found at {font_path}. Fallback fonts will be used.", file=sys.stderr)

def format_label(val, diff, pct, calculate_mom):
    if not calculate_mom:
        return f"{int(val):,}"
    if pd.isna(diff):
        return f"{int(val):,}"
    sign = "+" if diff > 0 else ""
    return f"{int(val):,}\n{sign}{int(diff):,} ({sign}{pct}%)"

def generate_graph(json_str):
    try:
        config = json.loads(json_str)
        output_filename = config['output_filename']
        title = config.get('title', 'Graph')
        x_label = config.get('x_label', '')
        y_label = config.get('y_label', '')
        chart_type = config.get('chart_type', 'line')
        calculate_mom = config.get('calculate_mom', False)
        raw_data = config['data']
        series_config = config['series']
        x_axis_col = config['x_axis_col']
        
        df = pd.DataFrame(raw_data)
        
        is_datetime = False
        try:
            df[x_axis_col] = pd.to_datetime(df[x_axis_col])
            is_datetime = True
        except:
            pass
            
        plt.figure(figsize=(16, 10))
        
        if calculate_mom:
            for s in series_config:
                col = s['column']
                df[f'{col}_diff'] = df[col].diff()
                df[f'{col}_pct'] = (df[col].pct_change() * 100).round(1)

        if chart_type == 'line':
            for i, s in enumerate(series_config):
                col = s['column']
                color = s.get('color', '#5C3225') # Default to Cocoa brown
                plt.plot(df[x_axis_col], df[col], label=s['label'], marker='o', linewidth=4, markersize=10, color=color)
                
                for idx in range(len(df)):
                    diff = df[f'{col}_diff'][idx] if calculate_mom else None
                    pct = df[f'{col}_pct'][idx] if calculate_mom else None
                    lbl = format_label(df[col][idx], diff, pct, calculate_mom)
                    
                    va = 'bottom' if i % 2 == 0 else 'top'
                    y_val = df[col][idx]
                    y_range = df[col].max() - df[col].min()
                    offset = y_range * 0.05 if i % 2 == 0 else -y_range * 0.05
                    
                    plt.text(df[x_axis_col][idx], y_val + offset, lbl, ha='center', va=va, fontsize=18, color=color, fontweight='bold')
                    
        elif chart_type == 'bar':
            x = np.arange(len(df))
            width = 0.8 / len(series_config)
            
            ax = plt.gca()
            for i, s in enumerate(series_config):
                col = s['column']
                color = s.get('color', '#5C3225') # Default to Cocoa brown
                offset = (i - len(series_config)/2 + 0.5) * width
                bars = ax.bar(x + offset, df[col], width, label=s['label'], color=color)
                
                for idx in range(len(df)):
                    y_val = df[col][idx]
                    lbl = f"{int(y_val):,}"
                    # Print label slightly above the bar
                    ax.text(x[idx] + offset, y_val + (df[col].max() * 0.02), lbl, ha='center', va='bottom', fontsize=20, color=color, fontweight='bold')
            
            if is_datetime:
                plt.xticks(x, df[x_axis_col].dt.strftime('%B -%y'), rotation=45)
            else:
                plt.xticks(x, df[x_axis_col], rotation=45)
        
        plt.title(title, fontsize=32, fontweight='bold', color='#4A2C2A') # Tulip chocolate color
        plt.xlabel(x_label, fontsize=24, color='#4A2C2A')
        plt.ylabel(y_label, fontsize=24, color='#4A2C2A')
        
        ymin, ymax = plt.ylim()
        # Add a bit of headroom for labels
        plt.ylim(ymin, ymax * 1.15)
        
        if is_datetime and chart_type == 'line':
            plt.xlim(df[x_axis_col].min() - pd.Timedelta(days=15), df[x_axis_col].max() + pd.Timedelta(days=15))
            plt.xticks(df[x_axis_col], df[x_axis_col].dt.strftime('%B -%y'), rotation=45)
        elif chart_type == 'line':
            plt.xticks(rotation=45)
        
        plt.legend(loc='upper left', prop={'size': 18})
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        
        plt.savefig(output_filename, dpi=300)
        print(f"Success: Graph saved to {output_filename}")

    except Exception as e:
        print(f"Error generating graph: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a graph from JSON configuration.')
    parser.add_argument('json_params', type=str, help='JSON string containing configuration.')
    args = parser.parse_args()
    generate_graph(args.json_params)
