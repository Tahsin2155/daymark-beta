# ============================================================================
# ANALYTICS & VISUALIZATION MODULE
# ============================================================================
# This file creates all the charts and graphs for the Analytics tab.
#
# CHARTS WE CREATE:
# 1. Daily Score Chart   → Line graph showing habits completed per day
# 2. Habit Consistency   → Bar chart showing total completions per habit
# 3. Individual Trends   → Line graph comparing selected habits over time
#
# LIBRARIES USED:
# - Plotly: A powerful charting library that creates interactive graphs
# - Streamlit's @st.cache_data: Caches results to avoid recalculating
#
# CACHING:
# Charts are cached for 60 seconds. This means if you view the same data
# multiple times, it won't recalculate - it just shows the cached result.
# ============================================================================

import plotly.graph_objects as go  # Plotly for creating charts
import streamlit as st  # For caching decorator


# ----------------------------------------------------------------------------
# DAILY SCORE CALCULATION & CHART
# ----------------------------------------------------------------------------

@st.cache_data(ttl=60)  # Cache for 60 seconds to avoid recalculating
def calculate_daily_score(habits_data):
    """
    Calculate how many habits were completed each day of the month.
    
    Args:
        habits_data (dict): All habits data in format:
            {"Gym": {"1": True, "2": False, ...}, "Read": {"1": True, ...}}
    
    Returns:
        plotly.graph_objects.Figure: A line chart of daily scores
    
    Example:
        If you have 3 habits and completed 2 on day 1, daily_scores["1"] = 2
    """
    daily_scores = {}
    
    # Loop through each possible day (1 to 31)
    for day in range(1, 32):
        day_str = str(day)  # Convert to string since our keys are strings
        score = 0
        
        # Check each habit to see if it was done on this day
        for habit_name, days_dict in habits_data.items():
            # If this day exists and the value is True, increment score
            if day_str in days_dict and days_dict[day_str]:
                score += 1
        
        daily_scores[day_str] = score
    
    # Create and return the chart
    return plot_daily_score(daily_scores)


# ----------------------------------------------------------------------------
# HABIT CONSISTENCY CALCULATION & CHART
# ----------------------------------------------------------------------------

@st.cache_data(ttl=60)  # Cache for 60 seconds
def calculate_habit_consistency(habits_data):
    """
    Calculate how many times each habit was completed this month.
    
    This shows you which habits you're most consistent with (the "winners").
    
    Args:
        habits_data (dict): All habits data
    
    Returns:
        plotly.graph_objects.Figure: A bar chart of habit totals
    
    Example:
        If "Gym" was True on 20 days, habit_totals["Gym"] = 20
    """
    habit_totals = {}
    
    # Loop through each habit
    for habit_name, days_dict in habits_data.items():
        # Count how many True values (completed days) this habit has
        # The 'if value' part filters to only True values
        total = sum(1 for value in days_dict.values() if value)
        habit_totals[habit_name] = total
    
    # Create and return the chart
    return plot_habit_consistency(habit_totals)


# ----------------------------------------------------------------------------
# CHART CREATION FUNCTIONS
# ----------------------------------------------------------------------------
# These functions take calculated data and create Plotly figures.

def plot_daily_score(daily_scores):
    """
    Create a LINE CHART showing daily habit completion scores.
    
    This chart helps you see patterns in your productivity:
    - Which days are you most productive?
    - Are weekends different from weekdays?
    - Is there a trend over the month?
    
    Args:
        daily_scores (dict): {"1": 3, "2": 2, "3": 4, ...} (day -> count)
    
    Returns:
        plotly.graph_objects.Figure: The line chart
    """
    # Extract days and scores as lists for plotting
    days = list(daily_scores.keys())
    scores = list(daily_scores.values())
    
    # Create an empty figure
    fig = go.Figure()
    
    # Add a line trace (the actual line on the chart)
    fig.add_trace(go.Scatter(
        x=days,                          # X-axis: day numbers
        y=scores,                        # Y-axis: scores
        mode='lines+markers',            # Show both line and dots
        name='Daily Score',              # Name shown in legend
        line=dict(color='#1f77b4', width=2),  # Blue line, 2px thick
        marker=dict(size=8)              # Dot size
    ))
    
    # Customize the chart's appearance
    fig.update_layout(
        title='Total Daily Score (Habits Completed Per Day)',
        xaxis_title='Day of Month',
        yaxis_title='Number of Habits Completed',
        hovermode='x unified',  # When hovering, show all values for that day
        height=400              # Chart height in pixels
    )
    
    return fig


def plot_habit_consistency(habit_totals):
    """
    Create a BAR CHART showing total completions per habit.
    
    This chart shows which habits you're best at maintaining.
    Habits are sorted so the "winner" (most completions) is first.
    
    Args:
        habit_totals (dict): {"Gym": 20, "Read": 18, ...}
    
    Returns:
        plotly.graph_objects.Figure: The bar chart
    """
    habits = list(habit_totals.keys())
    totals = list(habit_totals.values())
    
    # Sort habits by total completions (highest first)
    sorted_data = sorted(zip(habits, totals), key=lambda x: x[1], reverse=True)
    habits, totals = zip(*sorted_data) if sorted_data else ([], [])
    
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=habits,                        # X-axis: habit names
        y=totals,                        # Y-axis: completion counts
        marker=dict(
            color=totals,                # Color intensity based on value
            colorscale='Viridis',        # Green → yellow → purple gradient
            showscale=True               # Show the color legend
        ),
        text=totals,                     # Show numbers on top of bars
        textposition='outside'           # Numbers appear above bars
    ))
    
    fig.update_layout(
        title='Habit Consistency - Who\'s the Winner?',
        xaxis_title='Habits',
        yaxis_title='Total Completions',
        height=400,
        showlegend=False                 # No legend needed for bar chart
    )
    
    return fig


# ----------------------------------------------------------------------------
# INDIVIDUAL HABIT TRENDS CHART
# ----------------------------------------------------------------------------

def plot_individual_trends(habits_data, selected_habits):
    """
    Create a LINE CHART comparing specific habits over time.
    
    Users can select which habits to display using checkboxes.
    Each habit gets its own colored line.
    
    Args:
        habits_data (dict): All habits data
        selected_habits (list): Names of habits to show (e.g., ["Gym", "Read"])
    
    Returns:
        plotly.graph_objects.Figure: The comparison line chart
    """
    fig = go.Figure()
    
    # Define colors for each line (cycles if more than 5 habits)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    #          blue       orange     green      red        purple
    
    # Add a line for each selected habit
    for idx, habit_name in enumerate(selected_habits):
        days_dict = habits_data.get(habit_name, {})
        
        # Get sorted day numbers and convert True/False to 1/0
        days = sorted([int(d) for d in days_dict.keys()])
        values = [1 if days_dict[str(d)] else 0 for d in days]
        
        # Add this habit's line to the chart
        fig.add_trace(go.Scatter(
            x=days,
            y=values,
            mode='lines+markers',
            name=habit_name,                              # Shows in legend
            line=dict(color=colors[idx % len(colors)], width=2),
            marker=dict(size=6)
        ))
    
    # Customize the chart
    fig.update_layout(
        title='Individual Habit Trends - Daily Completion',
        xaxis_title='Day of Month',
        yaxis_title='Completed (1) or Not (0)',
        hovermode='x unified',
        height=400,
        yaxis=dict(
            tickvals=[0, 1],                # Only show 0 and 1 on Y-axis
            ticktext=['Not Done', 'Done']   # Label them nicely
        )
    )
    
    return fig