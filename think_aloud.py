import os
import openai
import whisper
openai.api_key = os.getenv("OPENAI_API_KEY")


def transcribe_audio(audio_files):
    model = whisper.load_model("medium")
    transcriptions = [model.transcribe(audio_file) for audio_file in audio_files]
    return transcriptions


def think_aloud_minutes(transcription):
    usability_issues = issues_extraction(transcription)
    actionable_insights = action_extraction(usability_issues, transcription)
    return {
        'usability_issues': usability_issues,
        'actionable_insights': actionable_insights,  
    }


def issues_extraction(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "As an AI with expertise in HCI, your task is to identify the main usability issues of a website from the following transcription from a usability test of a website. Based on the transcription provided, please identify and list the usability issues that users experienced while navigating or interacting with the website. Focus on points where users felt confused, frustrated, or encountered problems. Your goal is to provide a clear list of issues that can help designers understand areas that need improvement."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response['choices'][0]['message']['content']


def action_extraction(issues, transcription):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "As an AI with expertise in HCI, your task is to identify the main actionable insights to give designers of a website from the following transcription from a usability test of a website, as well as the previously extracted usability issues. Given the extracted usability issues and the transcription, please provide actionable insights or recommendations that the designers can implement to improve the website's usability. These should be practical steps or changes that can address the identified problems. Your goal is to help designers take effective actions to enhance the user experience."
            },
            {
                "role": "user",
                "content": f"""
                Issues extracted: {issues}
                transcription: {transcription}
                """
            }
        ]
    )
    return response['choices'][0]['message']['content']


def format_transcripts(transcripts):
    """
    Converts a list of transcripts into a readable string format for LLM processing.
    """
    formatted_transcripts = []
    for idx, transcript in enumerate(transcripts):
        formatted_transcript = f"Study {idx+1}:\n"
        formatted_transcript += f"Usability Issues: {transcript['usability_issues']}\n"
        formatted_transcript += f"Actionable Insights: {transcript['actionable_insights']}\n\n"
        formatted_transcripts.append(formatted_transcript)

    return "\n".join(formatted_transcripts)

def summarize_insights(transcripts):
    """
    transcripts: list of transcripts (combined output of multiple calls to think_aloud_minutes())
    """
    
    # Format transcripts for LLM
    all_transcripts = format_transcripts(transcripts)

    # Generate a summary based on all transcripts
    response = openai.Completion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are given a collection of usability studies for a website. Each study contains a list of usability issues identified from a think-aloud session and actionable insights recommended for addressing those issues. Based on this data, please provide a summarized list of key insights and common themes observed across all studies."
            },
            {
                "role": "user",
                "content": all_transcripts
            },
        ],
    )

    return response['choices'][0]['message']['content']




# def abstract_summary_extraction(transcription):
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following transcription from a usability test of a website and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
#             },
#             {
#                 "role": "user",
#                 "content": transcription
#             }
#         ]
#     )
#     return response['choices'][0]['message']['content']


# def key_points_extraction(transcription):
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following transcription from a usability test of a website, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about."
#             },
#             {
#                 "role": "user",
#                 "content": transcription
#             }
#         ]
#     )
#     return response['choices'][0]['message']['content']


# def sentiment_analysis(transcription):
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following transcription from a usability test of a website. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible."
#             },
#             {
#                 "role": "user",
#                 "content": transcription
#             }
#         ]
#     )
#     return response['choices'][0]['message']['content']