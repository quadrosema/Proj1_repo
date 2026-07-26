# AI Bio Generator

## 1. Project Overview

The AI Bio Generator is a small Flask web application that generates a short,
professional biography from three user-provided inputs: a person's name,
role, and hobbies. The app sends a structured prompt to a locally-run
Hugging Face text-generation model and returns a clean, 2-3 sentence bio
in the browser.

## 2. Technologies Used

- Python
- Transformers (Hugging Face)
- Torch (PyTorch)
- Flask

## 3. Model Information

- **Model:** `google/gemma-2-2b-it` (instruction-tuned)
- **Size:** ~2B parameters, loaded in FP16
- **Why this model was selected:** Gemma-2-2b-it is instruction-tuned, meaning
  it follows structured prompts (like the Name/Role/Hobbies template used
  here) far more reliably than smaller base models such as distilgpt2 or
  gpt2, which only continue text rather than follow instructions. It's
  small enough to run locally on a single machine while still producing
  coherent, on-topic output.

## 4. How the Model Works

A **prompt** is the text input given to the model that guides what it
generates next. For an instruction-tuned model like Gemma-2-2b-it, the
prompt is wrapped in a chat format (`{"role": "user", "content": ...}`)
so the model treats it as an instruction to follow rather than plain
text to continue.

This project uses **few-shot prompting**: the prompt includes two
worked examples of a name/role/hobbies bio before asking the model to
write one for the actual user input. Showing the model the desired
format directly produces more consistent, correctly-structured output
than simply describing the format in words (zero-shot).

The model generates text one token at a time — at each step it predicts
a probability distribution over possible next tokens, picks one
(deterministically or by sampling, depending on settings), appends it,
and repeats until it produces a stop signal or hits the token limit.

## 5. Parameter Tuning

Parameters used in the final app:

| Parameter | Value | Why |
|---|---|---|
| `max_new_tokens` | 150 | Enough headroom for a 2-3 sentence bio without cutting it off mid-sentence |
| `temperature` | 0.7 | Balanced setting — testing showed low (0.3) and high (1.2) temperatures produced similarly coherent output on this instruction-tuned model, so 0.7 was kept as a safe middle ground |
| `top_k` | 50 | Restricts sampling to the 50 most likely next tokens, preventing low-probability, off-topic words from being picked |
| `top_p` | 0.9 | Nucleus sampling — keeps the smallest set of tokens covering 90% probability mass, adapting the candidate pool size to the model's confidence at each step |
| `do_sample` | True | Enables sampling (temperature/top_k/top_p only take effect when this is True); tested against `do_sample=False` (greedy decoding), which produced comparably coherent but fully deterministic output |

Post-processing (`post.py` / `clean_bio()`) trims the raw model output to
a maximum number of sentences and removes duplicate sentences, since raw
generations occasionally repeated a phrase.

## 6. Example Input & Output

**Input:**
- Name: Amer
- Role: AI Engineer
- Hobbies: gaming

**Output:**
> Amer is an AI engineer who thrives on building intelligent systems and finding innovative solutions. When he's not immersed in algorithms and machine learning, he enjoys exploring the world of video games.

## 7. How to Run the Project

### Installation
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
hf auth login                   # required once - Gemma-2-2b-it is a gated model
```
Accept the model license at https://huggingface.co/google/gemma-2-2b-it
before logging in, or authentication will fail.

### Running the web application
```bash
cd src
python app.py
```
Then open `http://127.0.0.1:5000` in a browser, fill in Name/Role/Hobbies,
and submit to generate a bio.
