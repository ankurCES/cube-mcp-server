<!-- -->

# Cube MCP Server

Sample Repo for Connecting to Cube.dev pre-aggregations and makes time series data available to the LLM.

<!--  -->

## Steps

### Setup

Install `uv`

``` shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify Installation
``` shell
uv --version
```

Clone the repo and activate the virtual environment

``` shell
git clone https://github.com/ankurCES/cube-mcp-server
source .venv/bin/activate
```

Create the env file

``` shell 
cp sample.env.json env.json
```

Add the necessary configs and save.

Next run the below

``` shell
uv add "mcp[cli]" pandas pyarrow matplotlib requests PyJWT
```

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

``` shell
uv run main.py
```
