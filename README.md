# filesearch

A simple Flask application that uses the OpenAI API to look for user-specified content in images stored in a local folder.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your OpenAI API key.
3. Add images to the `images/` directory.
4. Run the application:
   ```bash
   python app.py
   ```
5. Open `http://localhost:5000` in your browser and search for the content you want.
