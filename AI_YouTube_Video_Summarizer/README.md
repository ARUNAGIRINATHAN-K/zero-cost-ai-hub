# AI YouTube Summarizer

This project is an AI-powered personal research assistant. It extracts the transcript from any YouTube video, processes it using a sliding window chunking strategy to bypass LLM token limits, and utilizes Google's `Flan-T5-Base` model to generate concise, bulleted notes summarizing the core content.

Instead of relying on paid APIs like OpenAI, this project demonstrates how to run an open-source Encoder-Decoder Large Language Model locally (or via Google Colab) using PyTorch and Hugging Face.

## Setup & Installation

```
!pip install -U youtube-transcript-api transformers accelerate sentencepiece
```

1. Install the required dependencies:

```Bash
pip install -r requirements.txt
```
Note: If you have an NVIDIA GPU, ensure you install the CUDA-compatible version of PyTorch for a ~10x speed increase during summarization.

2. Run the script:

```Bash
python main.py
```

## Architecture & Flow
1. **Data Extraction:** Parses YouTube URLs via Regex and pulls subtitle text using the `youtube-transcript-api`. Includes defensive programming to handle videos with disabled transcripts.
2. **Text Chunking:** Large transcripts exceed the context window of T5 models. The text is split into ~1200-character chunks, preserving sentence boundaries to avoid cutting off context mid-thought.
3. **Tokenization & Processing:** The text is passed through the `AutoTokenizer` and sent to the `cuda` device (if a GPU is available) for hardware-accelerated processing.
4. **Summarization via Beam Search:** The model generates summaries using `num_beams=4` and `length_penalty=1.0`. This ensures the model searches for the most logical sequence of words rather than just guessing the next word blindly.
