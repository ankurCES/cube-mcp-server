from server import mcp
from utils.cube_reader import main_runner

@mcp.tool()
def summarize_tag_data(tagname: str, plantcode: str, days_delta: int) -> str:
    environment = 'STAGING'
    return main_runner(plantcode, environment, tagname, days_delta)
