import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, render_template, request


load_dotenv()  # Loads the .env file
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

def get_ai_feedback(idea):
    prompt = f"""You're an expert startup advisor. A user submitted this startup idea:\n\n"{idea}"\n\nGive it a score out of 10 and a short helpful feedback. Format:\nScore: X/10\nFeedback: <one or two sentences>"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        feedback = response.choices[0].message.content
        return feedback
    except Exception as e:
        return f"Error: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    idea = ""

    if request.method == "POST":
        idea = request.form.get("idea", "")
        result = get_ai_feedback(idea)

    return render_template("index.html", result=result, idea=idea)

if __name__ == "__main__":
    app.run(debug=True)



