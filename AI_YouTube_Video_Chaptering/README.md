# AI YouTube Video Chaptering

The project aims to automatically segment a YouTube video into distinct, logical chapters with timestamps and titles by analyzing the video's transcript.

The pipeline works in four main steps:

1. **Data Extraction:** Fetch the video title and audio transcript using the YouTube Data API and YouTube Transcript API.
2. **Text Processing & Topic Modeling:** Use Non-negative Matrix Factorization (NMF) to find underlying topics within the transcript text.
3. **Logical Segmentation:** Compare the "dominant topic" of sequential text segments. If the topic changes and stays changed for a certain threshold (e.g., 60 seconds), it marks a chapter break.
4. **Chapter Naming:** Extract the most important keywords from each generated chapter segment using TF-IDF to create an automated title for that timestamp.

### **2. Libraries & Tech Stack**

Add these to your project's `requirements.txt`:

* **Data Collection APIs:**
    * `google-api-python-client` (YouTube Data API v3 for fetching video details)
    * `youtube-transcript-api` (For fetching the actual speech-to-text transcript)


* **Data Manipulation & Analysis:**
    * `pandas` (For structuring the transcript data and timestamps)
    * `numpy` (For numerical operations)
    * `matplotlib` (For optional data visualization, like text length distribution)


* **NLP & Machine Learning (scikit-learn):**
    * `CountVectorizer` (For finding common words and preparing text for NMF)
    * `TfidfVectorizer` (For extracting key phrases to name the chapters)
    * `NMF` (Non-negative Matrix Factorization for Topic Modeling)


* **Standard Python Libs:** `re`, `csv`

### **3. Setup & Installation**

1. Install the required dependencies:
```
pip install -r requirements.txt
```
2. Run thia to get transcript of a YouTube video

```
main.py
```
3. explore the collected dataset
```
app.ipynb
```

### **4. Enhancements for your Portfolio**

* **The Upgrade:** Instead of using TF-IDF to generate clunky chapter names, you should pass the text of that identified segment to the **Gemini API or OpenAI API**.
* **Why?** An LLM will read the segment and generate a perfect, human-readable chapter title (e.g., *"Understanding Muscle Failure"* instead of *"failure going way"*). This bridges the gap between traditional ML (segmentation) and GenAI (summarization), making your project vastly superior.