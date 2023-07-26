# chatify_server

This is a bastion server for the Chatify notebook explanation service, which uses LLMs to produce natural language exploration of a code notebook.

## Installation

```bash
poetry install
```

Before you can use the server, you must either (1) change the assignment and response stores in `server.py` to run locally (e.g., JSON stores), or (2) update the AWS credentials in the `config.py` file. Note that no `config.py` is provided; **you must create a new file.** But we do provide a [`config.example.py`](config.example.py) file that you can use as a template. See that file for itemwise documentation of the configuration options.

## Usage

For development server usage (with live reloads), run:

```bash
poetry run server-debug
# or:
# poetry run uvicorn freetext.server:app --reload --port 9900
```

For production server usage, run:

```bash
poetry run uvicorn freetext.server:app --port 9900
```
