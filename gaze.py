import os
import pandas as pd
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def filter_tsv(file_path):

    # Load TSV file
    data = pd.read_csv(file_path, sep='\t')  

    # Identify columns to remove
    columns_to_remove = [col for col in data.columns if data[col].nunique() <= 1]

    # Get values of removed columns
    removed_values = {col: data[col].iloc[0] for col in columns_to_remove}

    # Remove those columns 
    data_filtered = data.drop(columns=columns_to_remove)

    # Export filtered data to CSV file 
    new_file_path = file_path.replace(".tsv", ".csv")
    data_filtered.to_csv(new_file_path, index=False)

    return new_file_path, removed_values


def filter_time(file_path, start_time, end_time, output_path):
    """
    Filters a CSV file based on the LocalTimeStamp range.
    
    Parameters:
    - file_path (str): Path to the input TSV file.
    - start_time (str): Start time in the format 'HH:MM:SS.fff'.
    - end_time (str): End time in the format 'HH:MM:SS.fff'.
    - output_path (str): Path to save the output CSV file.
    
    Returns:
    - str: Path to the output CSV file.
    """
    
    # Load the TSV file
    data = pd.read_csv(file_path)
    
    # Filter the rows based on the specified time range
    filtered_data = data[
        (data['LocalTimeStamp'].str[-12:] >= start_time) &
        (data['LocalTimeStamp'].str[-12:] <= end_time)
    ]
    
    # Save the filtered data to the output CSV file
    filtered_data.to_csv(output_path, index=False)
    
    return output_path


import pandas as pd
import numpy as np

def calculate_number_of_fixations(filtered_data):
    # Assuming 'FixationIndex' column exists and a fixation is indicated by a non-empty and non-zero value
    return filtered_data['FixationIndex'].nunique()

def calculate_saccade_to_fixation_ratio(filtered_data):
    # Assuming 'SaccadeIndex' column exists and a saccade is indicated by a non-empty and non-zero value
    num_saccades = filtered_data['SaccadeIndex'].nunique()
    num_fixations = calculate_number_of_fixations(filtered_data)
    return num_saccades / num_fixations if num_fixations > 0 else np.nan

def calculate_number_of_saccades(filtered_data):
    return filtered_data['SaccadeIndex'].nunique()

def calculate_task_completion_time(filtered_data):
    # Assuming 'LocalTimeStamp' column exists and is already converted to datetime
    start_time = filtered_data['LocalTimeStamp'].min()
    end_time = filtered_data['LocalTimeStamp'].max()
    return (end_time - start_time).total_seconds()

def calculate_time_until_first_click(filtered_data):
    # Assuming 'MouseEventIndex' indicates clicks and 'LocalTimeStamp' is in datetime format
    first_click_time = filtered_data[filtered_data['MouseEventIndex'] > 0]['LocalTimeStamp'].min()
    task_start_time = filtered_data['LocalTimeStamp'].min()
    return (first_click_time - task_start_time).total_seconds()

def calculate_mean_time_between_clicks(filtered_data):
    # Assuming 'MouseEventIndex' indicates clicks and 'LocalTimeStamp' is in datetime format
    click_times = filtered_data[filtered_data['MouseEventIndex'] > 0]['LocalTimeStamp']
    if len(click_times) > 1:
        return click_times.diff().mean().total_seconds()
    else:
        return np.nan

def calculate_number_of_mouse_clicks(filtered_data):
    # Assuming 'MouseEventIndex' indicates clicks
    return filtered_data['MouseEventIndex'].nunique()

def calculate_scanpath_length(filtered_data):
    # Assuming 'SaccadicAmplitude' column exists and it indicates the length of each saccade
    return filtered_data['SaccadicAmplitude'].sum()

def calculate_mousepath_length(filtered_data):
    # Check if there are mouse events
    if 'MouseEventX (MCSpx)' in filtered_data.columns and 'MouseEventY (MCSpx)' in filtered_data.columns:
        # Drop rows where the mouse event positions are NaN
        mouse_events = filtered_data.dropna(subset=['MouseEventX (MCSpx)', 'MouseEventY (MCSpx)'])

        # Calculate the differences between successive mouse event positions
        diff_x = mouse_events['MouseEventX (MCSpx)'].diff().fillna(0)
        diff_y = mouse_events['MouseEventY (MCSpx)'].diff().fillna(0)

        # Calculate the Euclidean distances and sum
        distances = (diff_x ** 2 + diff_y ** 2) ** 0.5
        total_length = distances.sum()

        return total_length
    else:
        # Return NaN if there are no mouse event position columns
        return np.nan


def filter_and_calculate_metrics(file_path, tasks, time_ranges, output_path):
    """
    Filters data by tasks and time ranges and calculates metrics for each task.

    Parameters:
    - file_path (str): Path to the input TSV file.
    - tasks (list): List of task names.
    - time_ranges (list of tuples): List of time range tuples (start_time, end_time).
    - output_path (str): Path to save the output CSV file.

    Returns:
    - str: Path to the output CSV file.
    """
    # Load the TSV file
    data = pd.read_csv(file_path)

    # Convert 'LocalTimeStamp' to datetime if it's not already
    data['LocalTimeStamp'] = pd.to_datetime(data['LocalTimeStamp'].str[-12:])

    # Prepare a DataFrame to store the results
    result_df = pd.DataFrame(columns=[
        "Task Name", "Number of Fixations Overall", "Saccade to Fixation Ratio",
        "Number of Saccades", "Task Completion Time (s)", "Time Until First Click (s)",
        "Mean Time Between Clicks (s)", "Number of Mouse Clicks",
        "Scanpath Length (px)", "Mousepath Length (px)"
    ])

    # Iterate over tasks and their corresponding time ranges
    for task, (start_time, end_time) in zip(tasks, time_ranges):
        # Filter data for the current task and time range
        task_data = data[(data['MediaName'] == task) &
                         (data['LocalTimeStamp'] >= start_time) &
                         (data['LocalTimeStamp'] <= end_time)]

        # Calculate metrics for the current task
        task_metrics = {
            "Task Name": task,
            "Number of Fixations Overall": calculate_number_of_fixations(task_data),
            "Saccade to Fixation Ratio": calculate_saccade_to_fixation_ratio(task_data),
            "Number of Saccades": calculate_number_of_saccades(task_data),
            "Task Completion Time (s)": calculate_task_completion_time(task_data),
            "Time Until First Click (s)": calculate_time_until_first_click(task_data),
            "Mean Time Between Clicks (s)": calculate_mean_time_between_clicks(task_data),
            "Number of Mouse Clicks": calculate_number_of_mouse_clicks(task_data),
            "Scanpath Length (px)": calculate_scanpath_length(task_data),
            "Mousepath Length (px)": calculate_mousepath_length(task_data)
        }

        # Create a DataFrame from the current task metrics
        current_task_df = pd.DataFrame([task_metrics])

        # Append the metrics for the current task to the result DataFrame
        result_df = pd.concat([result_df, current_task_df], ignore_index=True)


    # Save the results to the output CSV file
    result_df.to_csv(output_path, index=False)

    return output_path




def issues_extraction(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a seasoned usability analyst in evaluating website interactions with deep expertise in eye-tracking studies, NASA-TLX and SUS evaluations, and identifying patterns in user behavior that may suggest potential usability challenges."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']