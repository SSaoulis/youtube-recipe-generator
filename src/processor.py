
from components.get_transcript.get import get_transcript_from_url
from components.process_transcript.prompt import get_gemini_response

def process_url(url: str):
    
    transcript = get_transcript_from_url(url)
    response = get_gemini_response(transcript)
    return response

def main():
    url = "https://www.youtube.com/watch?v=VIdlVi-VzPY"
    output = process_url(url)

    with open("gemini_out.txt", "w") as f:
        f.write(output)

main()