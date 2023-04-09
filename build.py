import argparse
import logging

from dotenv import load_dotenv

from github_helper import clone_git_repo, get_github_link
from llmhelper import LangchainHelper

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(levelname)s %(message)s')
    parser = argparse.ArgumentParser(description='CLI for Langchain script')
    parser.add_argument('--github_link', type=str, required=False,
                        help='GitHub repository link (optional)')
    parser.add_argument('--reload', action='store_true',
                        help='Reload the git repository if set, otherwise use existing one')
    args = parser.parse_args()

    github_link = get_github_link(args.github_link)
    module_name = clone_git_repo(github_link, args.reload)
    langchain_helper = LangchainHelper(module_name=module_name)
