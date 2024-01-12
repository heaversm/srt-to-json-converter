import json
import os
import gradio as gr

def process_srt(file_path, podcast_name, podcast_episode):
    # Get the directory of the current script and go one level up
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)

    # Prepare the output path in the 'downloads' directory one level above script_dir
    output_dir = os.path.join(parent_dir, "downloads")
    base_name = os.path.basename(file_path).rsplit('.', 1)[0]
    output_file = os.path.join(output_dir, f"{base_name}.json")

    # Create the downloads directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process the SRT file
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    entries = srt_content.strip().split('\n\n')
    transcripts = []

    for entry in entries:
        lines = entry.split('\n')
        id = int(lines[0])
        timestamp = lines[1]
        timestamp_start, timestamp_end = timestamp.split(" --> ")
        transcript = ' '.join(lines[2:])
        transcripts.append({'podcast_name': podcast_name, 'podcast_episode': podcast_episode, 'line_id': id, 'timestamp_start': timestamp_start, 'timestamp_end': timestamp_end, 'content': transcript})

    json_data = transcripts

    # Save the output to the specified JSON file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, indent=2)

    return output_file

# Create the Gradio interface
interface = gr.Interface(
    fn=process_srt,
    inputs=[
        gr.File(type='filepath', label='Upload Transcript (.srt)'),
        gr.Textbox(label='Podcast Name'),
        gr.Textbox(label='Podcast Episode')
    ],
    outputs='file',
    title='SRT to JSON Converter',
    description='Upload an SRT file and enter the podcast name and episode to convert it to JSON format.'
)

interface.launch(share=True)