import logging
import os

from dotenv import load_dotenv
from github_helper import clone_git_repo
from llmhelper import LangchainHelper

if __name__ == '__main__':
    load_dotenv()
    github_link = os.environ.get('GITHUB_LINK')
    logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(levelname)s %(message)s')
    module_name = clone_git_repo(github_link, False)
    langchain_helper = LangchainHelper(module_name=module_name)
