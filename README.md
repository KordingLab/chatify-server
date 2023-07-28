# chatify_server

This is a bastion server for the Chatify notebook explanation service, which uses LLMs to produce natural language exploration of a code notebook.

## Installation

```bash
poetry install
```

Before you can use the server, you must either (1) change the assignment and response stores in `server.py` to run locally (e.g., JSON stores), or (2) update the AWS credentials in the `config.py` file. Note that no `config.py` is provided; **you must create a new file.** But we do provide a [`config.example.py`](chatify_server/config.example.py) file that you can use as a template. See that file for itemwise documentation of the configuration options.

## Usage

For production server usage, run:

```bash
poetry run uvicorn chatify_server.server:app --port 9910
```


<hr /><p align='center'><small>Made with 💚 at <a href='https://kordinglab.com/'> the Kording Lab <img alt='KordingLab.com' align='center' src='https://github.com/KordingLab/chatify-server/assets/693511/b073b7a7-745e-41d1-b5f6-7efe56109712' height='32px'></a></small></p>

