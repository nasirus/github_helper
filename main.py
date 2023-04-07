import argparse
import textwrap

from colorama import init, Fore
from dotenv import load_dotenv

import llmhelper
from github_helper import clone_git_repo


def main(bot_mode, github_link, question):
    load_dotenv()
    chat_history = []
    module_name = clone_git_repo(github_link, True)

    init(autoreset=True)  # Initialize colorama

    if bot_mode == "chat":
        chat_bot = llmhelper.LangchainHelper(module_name=module_name).initialize_chat_bot()
        print(f"Start chat with {module_name}, type your question")

        while True:
            query = input(Fore.GREEN + "-->")
            result = chat_bot({"question": query, "chat_history": chat_history})
            chat_history.append((query, result["answer"]))
            print_wrapped_text(Fore.BLUE + "-->" + result["answer"].lstrip())
    elif bot_mode == "qa":
        langchain_helper = llmhelper.LangchainHelper(module_name=module_name)
        result = langchain_helper.answer_simple_question(query=question)
        print(Fore.BLUE + result.lstrip())


def print_wrapped_text(text, width=80):
    wrapped_text = textwrap.fill(text, width=width)
    print(wrapped_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Langchain Chatbot and QA")
    parser.add_argument("--bot_mode", choices=["chat", "qa"], default="chat",
                        help="Choose the mode for the bot: 'chat' or 'qa'")
    parser.add_argument("--github_link", help="The GitHub link for the repository to clone",
                        default="https://github.com/nasirus/github_helper.git")
    parser.add_argument("--question", default="what is github helper?", help="The question to be answered in 'qa' mode")

    args = parser.parse_args()
    main(args.bot_mode, args.github_link, args.question)
