import os
import requests
from langchain.llms import AzureOpenAI


def chat_gpt_summarize(code):
    llm = AzureOpenAI(
        deployment_name="text-davinci-003",
        model_name="text-davinci-003",
        temperature=0,
        max_tokens=512,
    )

    prompt = f"Summarize the following Python code: ```python\n{code}\n```"

    response = llm(prompt)
    result = response[0]['text'].strip()
    return result


def generate_readme(project_folder):
    readme_filename = os.path.join(project_folder, "generated_doc.md")
    with open(readme_filename, "w") as readme_file:
        for root, dirs, files in os.walk(project_folder):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as python_file:
                        code = python_file.read()
                        summary = chat_gpt_summarize(code)
                        readme_file.write(f"## {file}\n\n{summary}\n\n")


if __name__ == "__main__":
    project_folder = "/"
    generate_readme(project_folder)
