import os
import pandas as pd
import openai
import numpy as np
from scipy.spatial.distance import euclidean
openai.api_key = os.getenv("OPENAI_API_KEY")

def split_recordings_to_tsv(input_tsv_file):
    # Read the TSV file
    df = pd.read_csv(input_tsv_file, sep='\t')
    
    # Initialize an empty list to keep track of dataframes for each recording
    recording_dfs = []
    
    # Initialize indices for slicing the DataFrame according to recording events
    start_index = None
    
    # Iterate over the DataFrame to find start and stop events
    for index, row in df.iterrows():
        if row['StudioEvent'] == 'ScreenRecStarted':
            start_index = index
        elif row['StudioEvent'] == 'ScreenRecStopped' and start_index is not None:
            # Slice the DataFrame for the current recording
            recording_dfs.append(df[start_index:index + 1])
            start_index = None  # Reset start index for the next recording
    
    # Save each recording to a separate TSV file
    for i, recording_df in enumerate(recording_dfs):
        output_file = f'{input_tsv_file}_{i+1}.tsv'
        recording_df.to_csv(output_file, sep='\t', index=False)
        print(f'Saved: {output_file}')



def time_to_first_fixation(df):
    """Calculate the time to the first fixation."""
    first_fixation_time = df[df['GazeEventType'] == 'Fixation']['RecordingTimestamp'].min()
    return first_fixation_time

def fixation_duration(df):
    """Calculate the total duration of each fixation."""
    fixation_durations = df[df['GazeEventType'] == 'Fixation'].groupby('FixationIndex')['GazeEventDuration'].sum()
    return fixation_durations

def number_of_fixations(df):
    """Count the number of fixations."""
    return df['FixationIndex'].nunique()

def saccade_to_fixation_ratio(df):
    """Calculate the ratio of saccades to fixations."""
    num_saccades = df[df['GazeEventType'] == 'Saccade']['SaccadeIndex'].nunique()
    num_fixations = number_of_fixations(df)
    return num_saccades / num_fixations if num_fixations else 0

def number_of_saccades(df):
    """Count the number of saccades."""
    return df['SaccadeIndex'].nunique()

def saccade_amplitude(df):
    """Calculate the amplitude of saccades."""
    saccades = df[df['GazeEventType'] == 'Saccade']
    amplitudes = saccades['SaccadicAmplitude']
    return amplitudes

def scan_path_length(df):
    """Calculate the total scan path length."""
    fixation_points = df[df['GazeEventType'] == 'Fixation'][['FixationPointX (MCSpx)', 'FixationPointY (MCSpx)']].dropna()
    path_length = sum(euclidean(fixation_points.iloc[i], fixation_points.iloc[i+1])
                      for i in range(len(fixation_points)-1))
    return path_length

def spatial_density_of_scan_path(df):
    """Calculate the spatial density of the scan path."""
    # This can be a complex metric depending on your definition; here's a simple version
    # that calculates the average distance between consecutive fixations.
    fixation_points = df[df['GazeEventType'] == 'Fixation'][['FixationPointX (MCSpx)', 'FixationPointY (MCSpx)']].dropna()
    distances = [euclidean(fixation_points.iloc[i], fixation_points.iloc[i+1])
                 for i in range(len(fixation_points)-1)]
    return np.mean(distances) if distances else 0

def total_fixation_time(df):
    """Calculate the total time spent on fixations."""
    total_time = df[df['GazeEventType'] == 'Fixation']['GazeEventDuration'].sum()
    return total_time

def ratio_of_eye_path_to_task_length(df):
    """Calculate the ratio of eye-path length to length of task."""
    # Calculate task length
    task_start_time = df['RecordingTimestamp'].min()
    task_end_time = df['RecordingTimestamp'].max()
    task_length = (task_end_time - task_start_time) / 1000.0  # Convert from ms to seconds

    # Calculate scan path length
    path_length = scan_path_length(df)
    
    # Calculate the ratio
    ratio = path_length / task_length if task_length > 0 else None
    return ratio

def mean_pupil_size(df):
    """
    Calculate the mean pupil size.
    This function assumes that the DataFrame has 'PupilLeft' and 'PupilRight' columns.
    """
    
    # Clean the data: remove rows where pupil size is missing or zero (which may indicate blinks or recording errors)
    clean_df = df[(df['PupilLeft'] > 0) & (df['PupilRight'] > 0)]
    
    # Calculate the mean pupil size for each row
    clean_df['MeanPupilSize'] = clean_df[['PupilLeft', 'PupilRight']].mean(axis=1)
    
    # Calculate the overall mean pupil size
    overall_mean = clean_df['MeanPupilSize'].mean()
    
    return overall_mean

def task_analysis(input_tsv_file):
    # Read the TSV file
    df = pd.read_csv(input_tsv_file, sep='\t')
    
    # Calculate metrics
    metrics = {
        'time_to_first_fixation': time_to_first_fixation(df),
        'fixation_duration': fixation_duration(df),
        'number_of_fixations': number_of_fixations(df),
        'saccade_to_fixation_ratio': saccade_to_fixation_ratio(df),
        'number_of_saccades': number_of_saccades(df),
        'saccade_amplitude': saccade_amplitude(df),
        'scan_path_length': scan_path_length(df),
        'spatial_density_of_scan_path': spatial_density_of_scan_path(df),
        'total_fixation_time': total_fixation_time(df),
        'ratio_of_eye_path_to_task_length': ratio_of_eye_path_to_task_length(df),
        'mean_pupil_size': mean_pupil_size(df),
    }
    
    # Print metrics
    for metric_name, metric_value in metrics.items():
        print(f'{metric_name}: {metric_value}')

    return metrics

def website_analysis(input_tsv_files):
    # Read the TSV files
    dfs = [pd.read_csv(input_tsv_file, sep='\t') for input_tsv_file in input_tsv_files]
    
    # Calculate metrics
    metrics = {
        'time_to_first_fixation': [time_to_first_fixation(df) for df in dfs],
        'fixation_duration': [fixation_duration(df) for df in dfs],
        'number_of_fixations': [number_of_fixations(df) for df in dfs],
        'saccade_to_fixation_ratio': [saccade_to_fixation_ratio(df) for df in dfs],
        'number_of_saccades': [number_of_saccades(df) for df in dfs],
        'saccade_amplitude': [saccade_amplitude(df) for df in dfs],
        'scan_path_length': [scan_path_length(df) for df in dfs],
        'spatial_density_of_scan_path': [spatial_density_of_scan_path(df) for df in dfs],
        'total_fixation_time': [total_fixation_time(df) for df in dfs],
        'ratio_of_eye_path_to_task_length': [ratio_of_eye_path_to_task_length(df) for df in dfs],
        'mean_pupil_size': [mean_pupil_size(df) for df in dfs],
    }
    



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