import plotly.graph_objects as go


def calculate_daily_score(habits_data):
    """
    Calculate how many habits were completed each day.
    
    Input: {"Gym": {"1": True, "2": False, ...}, "Read": {"1": True, ...}}
    Output: {"1": 2, "2": 1, "3": 2, ...}  <- number of habits done per day
    """
    daily_scores = {}
    
    # Loop through each day (1 to 31)
    for day in range(1, 32):
        day_str = str(day)
        score = 0
        
        # Count how many habits were True on this day
        for habit_name, days_dict in habits_data.items():
            if day_str in days_dict and days_dict[day_str]:
                score += 1
        
        daily_scores[day_str] = score
    
    return plot_daily_score(daily_scores)


def calculate_habit_consistency(habits_data):
    """
    Calculate total completions per habit (who's the "winner").
    
    Input: {"Gym": {"1": True, "2": False, ...}, "Read": {"1": True, ...}}
    Output: {"Gym": 20, "Read": 18, "Meditate": 15}  <- total completions
    """
    habit_totals = {}
    
    for habit_name, days_dict in habits_data.items():
        # Count True values for this habit across all days
        total = sum(1 for value in days_dict.values() if value)
        habit_totals[habit_name] = total
    
    return plot_habit_consistency(habit_totals)



def plot_daily_score(daily_scores):
    """
    Total Graph

    Shows a line chart of daily productivity.
    X-axis: Day of month (1-31)
    Y-axis: Number of habits completed
    """
    days = list(daily_scores.keys())
    scores = list(daily_scores.values())
    
    fig = go.Figure()
    
    # Add line trace
    fig.add_trace(go.Scatter(
        x=days,
        y=scores,
        mode='lines+markers',  # Both lines and dots
        name='Daily Score',
        line=dict(color='#1f77b4', width=2),  # Blue color
        marker=dict(size=8)
    ))
    
    # Customize layout
    fig.update_layout(
        title='Total Daily Score (Habits Completed Per Day)',
        xaxis_title='Day of Month',
        yaxis_title='Number of Habits Completed',
        hovermode='x unified',  # Show all values when hovering
        height=400
    )
    
    return fig


def plot_habit_consistency(habit_totals):
    """
    Bar Graph

    Shows a bar chart of total completions per habit.
    X-axis: Habit names
    Y-axis: Total completions
    """
    habits = list(habit_totals.keys())
    totals = list(habit_totals.values())
    
    # Sort by totals descending (winner first)
    sorted_data = sorted(zip(habits, totals), key=lambda x: x[1], reverse=True)
    habits, totals = zip(*sorted_data)
    
    fig = go.Figure()
    
    # Add bar trace
    fig.add_trace(go.Bar(
        x=habits,
        y=totals,
        marker=dict(
            color=totals,  # Color intensity based on height
            colorscale='Viridis',  # Green to purple gradient
            showscale=True
        ),
        text=totals,  # Show numbers on top of bars
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Habit Consistency - Who\'s the Winner?',
        xaxis_title='Habits',
        yaxis_title='Total Completions',
        height=400,
        showlegend=False
    )
    
    return fig


def plot_individual_trends(habits_data, selected_habits):
    """
    Per Habit Graph
    
    Shows line chart comparing specific habits' daily trends.
    
    Args:
        habits_data: {"Gym": {"1": True, "2": False, ...}, ...}
        selected_habits: ["Gym", "Read"]  <- user selected these
    """
    fig = go.Figure()
    
    # Define colors for different habits
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Add a line for each selected habit
    for idx, habit_name in enumerate(selected_habits):
        days_dict = habits_data.get(habit_name, {})
        
        # Convert to numeric (True=1, False=0) for visualization
        days = sorted([int(d) for d in days_dict.keys()])
        values = [1 if days_dict[str(d)] else 0 for d in days]
        
        fig.add_trace(go.Scatter(
            x=days,
            y=values,
            mode='lines+markers',
            name=habit_name,
            line=dict(color=colors[idx % len(colors)], width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title='Individual Habit Trends - Daily Completion',
        xaxis_title='Day of Month',
        yaxis_title='Completed (1) or Not (0)',
        hovermode='x unified',
        height=400,
        yaxis=dict(
            tickvals=[0, 1],
            ticktext=['Not Done', 'Done']
        )
    )
    
    return fig