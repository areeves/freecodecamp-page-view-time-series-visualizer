import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
df = df[ (df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975)) ]

month_order=["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    ax.plot(df)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample('ME').mean().reset_index()
    df_bar["year"] = df_bar.iloc[:, 0].dt.year
    df_bar["month"] = df_bar.iloc[:, 0].dt.strftime("%b")

    # Draw bar plot
    g = sns.catplot(
        data=df_bar,
        x="year",
        y=df_bar.columns[1],      # the 'value' column after resampling
        hue="month",
        hue_order=month_order,
        kind="bar",
        # height=figsize[1] / 1.2,   # approximate aspect control
        # aspect=figsize[0] / figsize[1],
        palette="tab20",
        legend_out=True
    )
    
    # Access the underlying figure and axes for OO control
    fig = g.fig
    ax = g.ax
    
    # Minimal customization
    ax.set_xlabel("Year")
    ax.set_ylabel('Page Views Per Month')
    ax.set_title('FCC Forum Page Views')
    
    # Improve legend
    g.legend.set_title("Month")
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig, axes = plt.subplots(1, 2, figsize=(15, 8))
    
    # Year-wise Box Plot (Trend)
    sns.boxplot(
        x='year', 
        y='value', 
        data=df_box, 
        ax=axes[0], 
        palette='tab10'
    )
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise Box Plot (Seasonality)
    sns.boxplot(
        x='month', 
        y='value', 
        data=df_box, 
        ax=axes[1], 
        order=month_order, 
        palette='tab10'
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    # Adjust layout for better spacing
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
