import os
import pandas as pd
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def filter_tsv(file_path):
    # Load the TSV file
    data = pd.read_csv(file_path, sep='\t')
    
    # Identify columns where all rows have the same value or contain no value
    columns_to_remove = [col for col in data.columns if data[col].nunique() <= 1]
    
    # Get the values of those columns
    removed_values = {col: data[col].iloc[0] for col in columns_to_remove}
    
    # Remove those columns from the DataFrame
    data_filtered = data.drop(columns=columns_to_remove)
    
    # Export the filtered data to a new TSV file
    new_file_path = file_path.replace(".tsv", "_filtered.tsv")
    data_filtered.to_csv(new_file_path, sep='\t', index=False)
    
    return new_file_path, removed_values


def filter_tsv(file_path, start_time, end_time, output_path):
    """
    Filters a TSV file based on the LocalTimeStamp range.
    
    Parameters:
    - file_path (str): Path to the input TSV file.
    - start_time (str): Start time in the format 'HH:MM:SS.fff'.
    - end_time (str): End time in the format 'HH:MM:SS.fff'.
    - output_path (str): Path to save the output CSV file.
    
    Returns:
    - str: Path to the output CSV file.
    """
    
    # Load the TSV file
    data = pd.read_csv(file_path, sep='\t')
    
    # Filter the rows based on the specified time range
    filtered_data = data[
        (data['LocalTimeStamp'].str[-12:] >= start_time) &
        (data['LocalTimeStamp'].str[-12:] <= end_time)
    ]
    
    # Save the filtered data to the output CSV file
    filtered_data.to_csv(output_path, index=False)
    
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