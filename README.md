# filesearch

Simple Flask app that searches a folder of images for content using OpenAI's vision capabilities.

## Setup

1. Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
cp .env.example .env
```

3. Place images to search inside `static/images/`.

## Running

```bash
python main.py
```

Then open your browser at `http://localhost:5000` and enter a search description.
