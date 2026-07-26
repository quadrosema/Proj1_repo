from flask import Flask, render_template, request
from transformers import pipeline
from post import clean_bio

app = Flask(__name__)


pipe = pipeline(
    "text-generation",
    model="google/gemma-2-2b-it",
    torch_dtype="float16",
    device_map="auto",
)


def build_prompt(name, role, hobbies):
    return f"""Write a short, professional biography based on the examples below. Keep it to 2-3 sentences, natural and specific, no generic filler phrases like "passionate about" or "when not immersed in".

Example 1:
Name: Sarah
Role: Data Scientist
Hobbies: hiking and reading
Bio: Sarah is a data scientist who turns messy datasets into clear, actionable insights. Outside of work, she trades spreadsheets for trail maps and good books.

Example 2:
Name: Ali
Role: Web Developer
Hobbies: gaming and photography
Bio: Ali builds fast, clean websites and enjoys the occasional late-night coding sprint. When he's not at the keyboard, he's behind a camera or deep in a game.

Now write a bio for:
Name: {name}
Role: {role}
Hobbies: {hobbies}
Bio:"""


def generate_bio(name, role, hobbies):
    prompt = build_prompt(name, role, hobbies)
    messages = [{"role": "user", "content": prompt}]
    result = pipe(
        messages,
        max_new_tokens=150,
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        do_sample=True,
    )
    raw_text = result[0]["generated_text"][-1]["content"]
    return clean_bio(raw_text)


@app.route("/", methods=["GET", "POST"])
def index():
    bio = None
    if request.method == "POST":
        name = request.form.get("name", "")
        role = request.form.get("role", "")
        hobbies = request.form.get("hobbies", "")
        bio = generate_bio(name, role, hobbies)

    return render_template("index.html", bio=bio)


if __name__ == "__main__":
    app.run(debug=True)