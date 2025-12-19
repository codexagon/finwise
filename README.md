# finwise

A slightly gamified finance tracking application built in Python using PySide6 and sqlite3.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/codexagon/finwise.git
cd finwise
```

2. Create a virtual environment and activate it:

```bash
python -m venv virtualenv
source virtualenv/bin/activate # for Linux & MacOS
.\virtualenv\Scripts\activate # for Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### AI Advisor Setup

4. Create a `.env` file in the project root and add the following text:

```bash
GEMINI_API_KEY=your_key_name
```

Get your API key from https://aistudio.google.com/app/api-keys

### Run the application

5. Run:

```bash
python main.py
```

## Features

- Track income & expenses
- Categorize transactions
- View summaries of spending patterns
- Store data locally using SQLite
- UI made using PySide6
- Integrated AI Advisor using Gemini:
  - Generates financial health assessments
  - Analyzes spending behaviour
  - Suggests savings tips & actionable items
