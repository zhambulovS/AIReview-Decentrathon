import re
import string
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

def getID(URL):
    id_capture_regex = (
        r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    )
    match = re.match(id_capture_regex, URL)
    if not match:
        raise ValueError("Invalid YouTube URL")
    return match.group(1)

def getTranscript(ID):
    try:
        transcript_dict = YouTubeTranscriptApi.get_transcript(ID)
        transcript_array = [chunk["text"] for chunk in transcript_dict]
        transcript_text_raw = " ".join(transcript_array)
        printable = set(string.printable)
        transcript_text = "".join(filter(lambda x: x in printable, transcript_text_raw))
        return transcript_text
    except Exception as e:
        return f"Error retrieving transcript: {e}"

def punctuateText(text):
    if any(punct in text for punct in ['.', ',', '!', '?']):  
        return text

    processedText = text.replace("&", "%26")
    try:
        cmd = subprocess.run(
            ["curl", "-d", f"text={processedText}", "http://bark.phon.ioc.ee/punctuator"],
            capture_output=True,
            encoding="utf8",
            shell=False 
        )
        if cmd.returncode == 0:
            return cmd.stdout
        else:
            return "Error with punctuator service"
    except Exception as e:
        return f"Error during punctuation process: {e}"

def smartTranscribe(URL):
    try:
        ID = getID(URL)
        transcript = getTranscript(ID)
        if "Error" in transcript:
            return transcript
        punctuatedTranscript = punctuateText(transcript)
        return punctuatedTranscript
    except ValueError as ve:
        return f"Invalid URL: {ve}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    URL = "https://www.youtube.com/watch?v=CqgmozFr_GM"
    print(smartTranscribe(URL))
