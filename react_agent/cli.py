import os

import click

from react_agent.core.agent import ReActAgent
from react_agent.core.llm_client import LLMClient
from react_agent.core.tools import get_default_tools
from react_agent.global_utils import get_llm_config


@click.command()
@click.argument(
    "project_directory",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
def main(project_directory):
    project_dir = os.path.abspath(project_directory)
    settings = get_llm_config()

    tools = get_default_tools()
    agent = ReActAgent(
        tools=tools,
        model=settings.model,
        client=LLMClient(settings=settings),
        project_directory=project_dir,
    )

    task = input("Input the task: ")
    final_answer = agent.run(task)
    print(f"\n\nFinal Answer: {final_answer}")


if __name__ == "__main__":
    main()