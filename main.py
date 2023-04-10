import argparse
import textwrap

from colorama import init, Fore
from dotenv import load_dotenv

import llmhelper
from github_helper import clone_git_repo, get_github_link


def main(bot_mode, git_link, question, reload_repo):
    chat_history = []
    module_name = clone_git_repo(git_link, reload_repo)

    init(autoreset=True)  # Initialize colorama

    langchain_helper = llmhelper.LangchainHelper(module_name=module_name)

    if bot_mode == "chat":
        chat_bot = langchain_helper.initialize_chat_bot()
        print_wrapped_text(Fore.BLUE + f"Start chat with {module_name}, type your question")

        while True:
            query = input(Fore.GREEN + "-->")
            result = chat_bot({"question": query, "chat_history": chat_history})
            chat_history.append((query, result["answer"]))
            print_wrapped_text(Fore.BLUE + "-->" + result["answer"].lstrip())
    elif bot_mode == "qa":
        result = langchain_helper.answer_simple_question(query=question)
        print_wrapped_text(Fore.BLUE + result.lstrip())


def print_wrapped_text(text, width=150):
    wrapped_text = textwrap.fill(text, width=width)
    print(wrapped_text)


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description="Langchain Chatbot and QA")
    parser.add_argument("--bot_mode", choices=["chat", "qa"], default="chat",
                        help="Choose the mode for the bot: 'chat' or 'qa'")
    parser.add_argument('--github_link', type=str, required=False,
                        help='GitHub repository link (optional)')
    parser.add_argument("--question", default="what is github helper?", help="The question to be answered in 'qa' mode")
    parser.add_argument('--reload', action='store_true', help='Reload the git repository if it already exists locally')

    args = parser.parse_args()
    github_link = get_github_link(args.github_link)
    main(args.bot_mode, github_link, args.question, args.reload)
