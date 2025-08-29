import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template, request
from openai import OpenAI

load_dotenv()

app = Flask(__name__, static_folder="images", static_url_path="/images")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

IMAGE_FOLDER = Path("images")


def image_contains_query(image_path: Path, query: str) -> bool:
    """Return True if OpenAI detects the query in the image."""
    with open(image_path, "rb") as image_file:
        img_b64 = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Does this image contain {query}? Answer yes or no.",
                    },
                    {"type": "input_image", "image": img_b64},
                ],
            }
        ],
    )
    result = response.output_text.strip().lower()
    return "yes" in result


@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        for image_file in IMAGE_FOLDER.iterdir():
            if image_file.is_file():
                try:
                    if image_contains_query(image_file, query):
                        matches.append(image_file.name)
                except Exception as exc:
                    print(f"Error processing {image_file}: {exc}")
    return render_template("index.html", matches=matches, query=query)


if __name__ == "__main__":
    app.run(debug=True)
