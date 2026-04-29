import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import sys
import argparse

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
        
        # Determine if x-axis is datetime
        is_datetime = False
        try:
            df[x_axis_col] = pd.to_datetime(df[x_axis_col])
            is_datetime = True
        except:
            # Keep as string/categorical if not datetime
            pass
            
        plt.figure(figsize=(14, 8))
        
        # Calculate MoM if requested
        if calculate_mom:
            for s in series_config:
                col = s['column']
                df[f'{col}_diff'] = df[col].diff()
                df[f'{col}_pct'] = (df[col].pct_change() * 100).round(1)

        if chart_type == 'line':
            for i, s in enumerate(series_config):
                col = s['column']
                color = s.get('color', '#36a2eb')
                plt.plot(df[x_axis_col], df[col], label=s['label'], marker='o', linewidth=2, color=color)
                
                # Add labels
                for idx in range(len(df)):
                    diff = df[f'{col}_diff'][idx] if calculate_mom else None
                    pct = df[f'{col}_pct'][idx] if calculate_mom else None
                    lbl = format_label(df[col][idx], diff, pct, calculate_mom)
                    
                    # Offset logic to avoid overlap (simple heuristic)
                    offset = 2000 if i % 2 == 0 else -2000
                    va = 'bottom' if i % 2 == 0 else 'top'
                    
                    # For a single line or specific tweaking, this might need adjustment based on y-scale, 
                    # but for absolute counts, we just place it slightly above/below
                    y_val = df[col][idx]
                    y_range = df[col].max() - df[col].min()
                    offset = y_range * 0.05 if i % 2 == 0 else -y_range * 0.05
                    
                    plt.text(df[x_axis_col][idx], y_val + offset, lbl, ha='center', va=va, fontsize=8, color=color, fontweight='bold')
                    
        elif chart_type == 'bar':
            x = np.arange(len(df))
            width = 0.8 / len(series_config)
            
            for i, s in enumerate(series_config):
                col = s['column']
                color = s.get('color', '#36a2eb')
                offset = (i - len(series_config)/2 + 0.5) * width
                plt.bar(x + offset, df[col], width, label=s['label'], color=color)
                
                # Add labels
                for idx in range(len(df)):
                    lbl = f"{int(df[col][idx]):,}"
                    plt.text(x[idx] + offset, df[col][idx] + (df[col].max() * 0.02), lbl, ha='center', va='bottom', fontsize=8, color=color, fontweight='bold')
            
            if is_datetime:
                plt.xticks(x, df[x_axis_col].dt.strftime('%B -%y'), rotation=45)
            else:
                plt.xticks(x, df[x_axis_col], rotation=45)
        
        plt.title(title, fontsize=16)
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel(y_label, fontsize=12)
        
        ymin, ymax = plt.ylim()
        plt.ylim(ymin, ymax * 1.15) # Add 15% headroom for labels
        
        # Adjust x-axis limit to avoid extending into the next month
        if is_datetime and chart_type == 'line':
            plt.xlim(df[x_axis_col].min() - pd.Timedelta(days=15), df[x_axis_col].max() + pd.Timedelta(days=15))
            # Explicitly set the x-axis ticks to ensure every data point is labelled exactly
            plt.xticks(df[x_axis_col], df[x_axis_col].dt.strftime('%B -%y'), rotation=45)
        elif chart_type == 'line':
            plt.xticks(rotation=45)
        
        plt.legend(loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
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
