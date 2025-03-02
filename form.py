import gradio as gr
import subprocess, threading
import shutil
import cv2
import librosa
from pydub import AudioSegment

def process_files(video_input, audio_input, progress=gr.Progress(track_tqdm=True)):
    if not video_input or not audio_input:
        return "Please upload both a video file and an audio file.", None, None
    
    video_output_path = "saved_video.mp4"
    shutil.copy(video_input, video_output_path)
    
    audio_output_path = "saved_audio.mp3"
    shutil.copy(audio_input, audio_output_path)
    
    # cap = cv2.VideoCapture(video_output_path)
    # frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    # mp4Duration = frame_count / fps
    
    # y, sr = librosa.load(audio_output_path, sr=None)
    # mp3Duration = librosa.get_duration(y=y, sr=sr)
    
    # silence_duration = max(0, mp4Duration - mp3Duration)
    
    # audio = AudioSegment.from_mp3(audio_output_path)
    # silence = AudioSegment.silent(duration=silence_duration)
    # extended_audio = audio + silence
    # extended_audio.export(audio_output_path, format="mp3")
    
    # y, sr = librosa.load(audio_output_path, sr=None)
    # mp3DurationAfter = librosa.get_duration(y=y, sr=sr)
    
    #return (text, video_output_path, audio_output_path);
    
    output = "results/result.mp4"
    command = [
        "python",
        "inference.py",
        "--face", video_output_path,
        "--audio", audio_output_path,
        "--outfile", output
    ]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #text = f'MP4 Duration: {mp4Duration}\nMP3 Duration before: {mp3Duration}\nMP3 Duration after: {mp3DurationAfter}'
        text = "ok"
        
        return (
            text,
            output
        )
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode("utf-8")
        return f"Error during processing:\n{error_message}", None
    

# Create the Gradio interface
with gr.Blocks() as demo:
    with gr.Row():
        # Left Column: Input components
        with gr.Column(scale=2):
            with gr.Row():
                with gr.Column(scale=1):
                    video_input = gr.Video(label="Video Control", format="mp4")
                with gr.Column(scale=1):
                    audio_input = gr.Audio(label="Audio Input", type="filepath")
        
            process_button = gr.Button("Process Files")
        
        # Right Column: Output components
        with gr.Column(scale=1):
            output_text = gr.Textbox(label="Processing Status", lines=10)
            audio_output = gr.Audio(label="Audio Output", type="filepath")
            video_output = gr.Video(label="Processed MP4 Output")

    # Link the button to the processing function
    process_button.click(
        fn=process_files,
        inputs=[video_input, audio_input],
        outputs=[output_text, video_output, audio_output]
    )

# Launch the Gradio app
demo.launch(share=True)
#demo.launch()