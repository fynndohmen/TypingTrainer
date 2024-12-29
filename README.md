TypingTrainer
TypingTrainer is an adaptive typing trainer application that uses local NLP tools (NLTK, Markovify, and optionally spaCy) to generate training texts and analyze typing performance. Unlike a solution powered by ChatGPT or external APIs, TypingTrainer works entirely offline once you have set up the necessary libraries and models.

How It Works
Typing Data Analysis: The program records typing times and errors per character to identify problematic characters, symbols, or numbers.
Local Text Generation: Instead of using an online API, TypingTrainer employs Markovify to generate new, fluid texts from a local text corpus. NLTK helps with statistical analysis (e.g., frequency of certain characters), while spaCy can add more complex linguistic analysis if needed.
Data Persistence: A local SQLite database (data/database.db) stores typing statistics for long-term tracking and improvement monitoring.


Requirements
Python Version: 3.8 or higher
Dependencies:
NLTK
Markovify
spaCy (optional for advanced language processing)
All required packages are listed in requirements.txt.



Project Structure
bash
Code kopieren
TypingTrainer/
│
├── main.py               # Entry point
├── requirements.txt      # Dependencies
├── README.md             # This documentation
│
├── app/
│   ├── __init__.py
│   ├── gui.py            # Tkinter GUI
│   ├── logic.py          # Core logic (coordinates data flow, typing analysis)
│   ├── data.py           # Database access (SQLite)
│   ├── text_generator.py # Local text generation using Markovify & NLTK analysis
│   ├── analysis.py       # Analysis of typing stats, problem characters, spaCy integration
│   └── config.py         # Configuration settings (e.g., paths, parameters)
│
├── data/
│   └── database.db       # SQLite database (created automatically if not present)
│
└── resources/
    ├── base_corpus.txt   # Base text corpus for Markovify
    └── stopwords.txt     # Optional: stopwords or additional lists



Installation & Setup
Clone the Repository:

git clone <repository-url>
cd TypingTrainer

Create a Virtual Environment:

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
Install Dependencies:

pip install -r requirements.txt
Install spaCy Language Model (Optional):

python -m spacy download en_core_news_sm


Usage
Start the program:

python main.py

A Tkinter window will open, allowing you to start typing exercises. The application measures typing speed, errors, and uses this data to adaptively generate new training texts.

Customization
Edit resources/base_corpus.txt to provide your own source texts for Markovify.
Adjust parameters in app/config.py (e.g., text length, training cycles, focus characters).
Modify analysis.py to incorporate more linguistic features via spaCy (like part-of-speech filtering or syntactic patterns).


Troubleshooting
If spacy.load("de_core_news_sm") fails, ensure you have run:
bash
Code kopieren
python -m spacy download de_core_news_sm
If using multiple Python installations, ensure you are in the correct virtual environment.
Confirm that all dependencies are installed in the active environment.


License & Contact
Author: Your Name
E-Mail: your-email@example.com
License: (Specify your chosen license, e.g., MIT or Apache 2.0)
GitHub Repository: [Link to your repository]