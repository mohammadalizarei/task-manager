# Task Manager AI Agent

A small practice project built with Python and the OpenAI Responses API.

The goal of this project is to learn how AI agents work and how they can use tools to perform tasks.

## Features

- Add, view, update, and delete tasks
- Set task priorities
- Manage events and meetings
- Work with dates and times
- Use AI tool calling to interact with the task manager

## Tech Stack

- Python
- OpenAI Responses API
- OpenAI Python SDK
- uv
- JSON for data storage

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd task-manager
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=your_base_url
```

Replace the values with your API credentials and model configuration.

### 4. Run the project

```bash
uv run python main.py
```

## Project Status

This is a practice project created for learning purposes. It is a work in progress and may not be suitable for production use.

## License

No license has been specified yet.
