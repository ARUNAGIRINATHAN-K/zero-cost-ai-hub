import re
import torch
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# ====================== REQUIREMENTS ======================
# pip install youtube-transcript-api transformers torch sentence-transformers
# ========================================================

def extract_video_id(url):
    """Extracts YouTube video ID from various URL formats."""
    patterns = [
        r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})",
        r"youtube\.com/.*[?&]v=([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(video_id):
    """Fetch transcript with better fallback handling."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Prefer manually created English, then auto-generated
        for transcript in transcript_list:
            if transcript.language_code.startswith('en'):
                fetched = transcript.fetch()
                return " ".join([item['text'] for item in fetched])
        
        # Fallback to first available
        transcript = transcript_list[0]
        fetched = transcript.fetch()
        return " ".join([item['text'] for item in fetched])

    except TranscriptsDisabled:
        return "Error: Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "Error: No transcript found for this video."
    except Exception as e:
        return f"Error: {str(e)}"


# Load model once (global)
device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "google/flan-t5-base"

print("Loading model (this may take a minute the first time)...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)


def summarize_chunk(text_chunk):
    """Generate summary for a chunk using Flan-T5."""
    prompt = f"Summarize the following text in clear, concise bullet points:\n\n{text_chunk}\n\nSummary:"

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024,
        padding=True
    ).to(device)

    summary_ids = model.generate(
        **inputs,
        max_new_tokens=150,
        num_beams=5,
        length_penalty=1.2,
        early_stopping=True,
        no_repeat_ngram_size=3
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True).strip()


def chunk_text(text, chunk_size=800):
    """Split text into chunks respecting sentence boundaries."""
    # Simple but effective sentence split
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []

    for sentence in sentences:
        if len(" ".join(current_chunk)) + len(sentence) < chunk_size:
            current_chunk.append(sentence)
        else:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def generate_video_notes(video_url):
    print(f"\n🎬 Processing video: {video_url}")

    video_id = extract_video_id(video_url)
    if not video_id:
        print("❌ Invalid YouTube URL.")
        return

    print("🎧 Fetching transcript...")
    transcript = get_transcript(video_id)

    if transcript.startswith("Error"):
        print(transcript)
        return

    print(f"✅ Transcript fetched ({len(transcript):,} characters)")

    print("🔪 Chunking transcript...")
    chunks = chunk_text(transcript)
    print(f"   -> Created {len(chunks)} chunks")

    print("🧠 Generating AI notes...")
    notes = []

    for i, chunk in enumerate(chunks):
        print(f"   Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk)
        if summary and not summary.lower().startswith("error"):
            notes.append(f"• {summary}")

    # Optional: Combine into final coherent notes
    print("\n" + "="*60)
    print("📝 AI-GENERATED VIDEO NOTES")
    print("="*60)
    print("\n".join(notes))
    print("\n✅ Done!")


if __name__ == "__main__":
    url = input("Paste YouTube URL: ").strip()
    if url:
        generate_video_notes(url)
    else:
        print("No URL provided.")