import re

from data.prompts import baseline_prompt, sys_prompt_2
from utils.utils import ask_gpt_4o, get_real_prompt

if __name__ == '__main__':
    prompts = []
    with open("data/original commands.csv", "r", encoding="utf-8") as original_commands:
        for command in original_commands:
            command = command.strip()

            original_prompt = get_real_prompt(baseline_prompt, command)
            # print(original_prompt)

            prompts.append(original_prompt)

    regularExpression = re.compile(r'"command": "(.*?)"')
    with open("data/modified command.csv", "w", encoding="utf-8") as modified_commands:
        for prompt in prompts:
            prompt = prompt.strip()

            response = ask_gpt_4o(sys_prompt_2, prompt)
            # print(response)

            match = re.search(regularExpression, response)
            if match is not None:
                modified_commands.write(match.group(1) + "\n")
            else:
                modified_commands.write("\n")
