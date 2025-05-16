<!-- -->

# Cube MCP Server

Sample Repo for Connecting to Cube.dev pre-aggregations and makes time series data available to the LLM.

<!--  -->

## Steps

### Setup

Install `uv`

`curl -LsSf https://astral.sh/uv/install.sh | sh`

Verify Installation
`uv --version`

Clone the repo and activate the virtual environment

`git clone <repo>`
`source .venv/bin/activate`

Create the env file

`cp sample.env.json env.json`

Add the necessary configs and save.

Next run the below

`uv add "mcp[cli]" pandas pyarrow matplotlib requests PyJWT`

### Add config for Claude Desktop

```json
{
  "mcpServers": {
    "mix_server": {
      "command": "path/to/uv",
      "args": ["--directory", "path/to/cube_server", "run", "main.py"]
    }
  }
}
```

### To Run

`uv run main.py`
