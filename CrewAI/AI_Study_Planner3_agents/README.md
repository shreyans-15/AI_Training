# AI Study Planner - CrewAI

A beginner-friendly three-agent CrewAI application.

## Workflow

1. Topic Explainer explains the selected Python topic and gives one small example.
2. Study Planner uses the first task output to prepare a three-day plan.
3. Quiz Creator uses the study plan to create exactly five questions without answers.

The crew uses `Process.sequential` and passes earlier task outputs through `context`.

## Setup

```bash
python -m venv venv
pip install -r requirements.txt
```

Activate the virtual environment, copy `.env.example` to `.env`, and enter
your Azure OpenAI configuration.

Run from this project folder:

```bash
python main.py
```

Enter a Python topic when prompted.
