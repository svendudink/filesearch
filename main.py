import os
import base64
from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

IMAGE_DIR = os.path.join('static', 'images')


def analyze_image(image_path: str, query: str) -> bool:
    """Ask OpenAI if the image contains the query text."""
    with open(image_path, 'rb') as img_file:
        b64 = base64.b64encode(img_file.read()).decode('utf-8')

    prompt = f"Does this image contain {query}? Answer yes or no."
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_base64": b64},
                ],
            }
        ],
    )

    answer = response.output_text.strip().lower()
    return answer.startswith("yes")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return redirect(url_for('index'))

    results = []
    for filename in os.listdir(IMAGE_DIR):
        path = os.path.join(IMAGE_DIR, filename)
        if os.path.isfile(path):
            try:
                if analyze_image(path, query):
                    results.append(os.path.join('images', filename))
            except Exception:
                # If OpenAI call fails, skip this image
                continue

    return render_template('index.html', results=results, query=query)


if __name__ == '__main__':
    app.run(debug=True)
