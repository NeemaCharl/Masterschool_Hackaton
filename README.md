# ChronoGuesser — History Trivia Game

ChronoGuesser is a Python command-line game that challenges players to identify historical people and events from redacted Wikipedia summaries. Play three rounds, request optional hints, and track scores in a local scoreboard.

> **Project note:** Your LinkedIn project description mentions a Wikipedia shortest-path game. The files currently in this repository describe a redacted-summary guessing game. If these are intended to be the same project, update the code or LinkedIn project entry so the public descriptions match.

## Features

- Three rounds per game, with a different historical article in each round.
- Redacted summaries and up to three guesses per round.
- Optional AI-generated hints, with up to two hints per round.
- Scoring that rewards correct answers and accounts for guesses and hints.
- A local JSON scoreboard.

## Requirements

- Python 3.8 or later
- `wikipedia` and `openai` Python packages
- An OpenAI API key in the environment if you want to use AI hints

Install dependencies:

```bash
python -m pip install wikipedia openai
```

## Run the game

From the repository root:

```bash
python "Chrono Guesser/ChronoGuesser_1.0.py"
```

Follow the terminal prompts to play. Type `hint` when prompted to request a hint. Scores are stored in `Chrono Guesser/scoreboard.json`.

## Configure AI hints

Set `OPENAI_API_KEY` before starting the game. Keep the key private and do not commit it to the repository.

macOS/Linux:

```bash
export OPENAI_API_KEY="your-api-key"
```

PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-api-key"
```

## Repository structure

```text
.
├── Chrono Guesser/
│   ├── ChronoGuesser_1.0.py
│   ├── list_of_articles.py
│   └── scoreboard.json
├── Walkthrough - ChronoGuesser.pages/
└── README.md
```

## Contributing

Open an issue to discuss a proposed change, then submit a focused pull request with a clear description and testing notes.

## License

No license is currently specified. Unless a license is added, reuse and redistribution are not granted by default.

---

Created for the Masterschool Hackathon by [Charles Nema](https://github.com/NeemaCharl).
