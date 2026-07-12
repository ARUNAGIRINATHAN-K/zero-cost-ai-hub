# Fine-Tuning Qwen3-4B with Unsloth [Kaggle Notebook](https://www.kaggle.com/code/arunsworkspace/fine-tuning-qwen3-4b-with-unsloth)

**Status:** 🚀 Completed  
**Tech Stack:** Python, PyTorch, Unsloth, Hugging Face (Transformers, TRL, Datasets), QLoRA, Groq API, Weights & Biases, ipywidgets.

## Overview
ProTutor is a custom 4-billion parameter AI tutor fine-tuned to teach software engineering concepts. This project demonstrates an end-to-end Large Language Model (LLM) distillation pipeline, leveraging a 120B parameter teacher model to generate synthetic training data, which is then used to fine-tune a smaller student model (Qwen3-4B). 

Built entirely on a free Kaggle T4 GPU, this pipeline utilizes QLoRA (Quantized Low-Rank Adaptation) and the Unsloth framework to optimize memory usage and accelerate training speed, completing the entire fine-tuning process in under 30 minutes.

## Setup & Installation
This project is designed to run natively on a Kaggle Notebook with a T4 GPU (×2) or any local Jupyter environment with at least 16GB VRAM. 

1. **Environment Setup (Kaggle):** Ensure Internet and GPU T4 are enabled in notebook settings.
2. **API Keys:** Add your free Groq API key to Kaggle Secrets as `GROQ_API_KEY`.
3. **Install Dependencies:**
   Run the following command to install the required stack (Note: Unsloth requires specific PyTorch/CUDA wheels):
   ```bash
   pip install -r requirements.txt

## Architecture & Flow

1. **Synthetic Data Generation (Distillation):** - Utilized the `openai/gpt-oss-120b` model via the **Groq API** to asynchronously generate ~300 high-quality question-answer pairs.
   - Enforced a strict zero-shot persona (standard English, universal analogies, specific summary formatting) without relying on system prompts at inference.
2. **Formatting & Tokenization:** - Serialized raw JSON data into the exact `ChatML` template (`<|im_start|>`, `<|im_end|>`) expected by the Qwen instruct model.
3. **Model Initialization & QLoRA:** - Loaded the `Qwen3-4B-Instruct` base model in **4-bit precision** using Unsloth.
   - Attached trainable LoRA matrices (Rank = 32) to the attention and MLP projections, targeting roughly 1.6% (66M) of the total model parameters.
4. **Training Loop:** - Executed supervised fine-tuning using TRL's `SFTTrainer`. 
   - Applied `train_on_responses_only` to mask the loss on user prompts, forcing the model to strictly optimize for the assistant's persona.
   - Tracked training loss and metrics via **Weights & Biases**.
5. **Interactive Evaluation & Export:** - Built a custom, interactive chat UI within the notebook using `ipywidgets` to test the held-out validation set.
   - Exported the final trained weights to **GGUF format** for local/edge deployment.