import argparse
import logging
import os

from flask import Flask, request, jsonify, render_template

from github_helper import github_reply, clone_git_repo
from llmhelper import LangchainHelper

app = Flask(__name__)

github_link = os.environ.get("GITHUB_LINK", "https://github.com/elastic/elasticsearch.git")

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(levelname)s %(message)s')

module_name = clone_git_repo(github_link, False)
langchain_helper = LangchainHelper(module_name=module_name)


@app.route('/github_webhook', methods=['POST'])
def github_webhook():
    data = request.get_json()

    if data['action'] == 'opened':
        repo_owner = data['repository']['owner']['login']
        repo_name = data['repository']['name']
        issue_number = data['issue']['number']
        issue_title = data['issue']['title']
        issue_comment = data['issue']['body']

        result = langchain_helper.assist_github_issue(issue_title=issue_title, issue_comment=issue_comment)
        print(result[0]['text'])

        github_reply(repo_owner=repo_owner, repo_name=repo_name, issue_number=issue_number,
                     comment_body=result[0]['text'])

    return "OK", 200


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_history = data.get('chat_history', [])
    query = data.get('question', '')
    chat_bot = langchain_helper.initialize_chat_bot()
    result = chat_bot({"question": query, "chat_history": chat_history})
    response = {
        "answer": result["answer"],
        "chat_history": chat_history + [(query, result["answer"])]
    }
    return jsonify(response)


@app.route('/qa', methods=['POST'])
def qa():
    data = request.get_json()
    question = data.get('question', '')
    result = langchain_helper.answer_simple_question(query=question)

    return jsonify({"result": result})


@app.route('/')
def index():
    return render_template('index.html', module_name=module_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI for Langchain script')
    parser.add_argument('--github_link', type=str, required=False, default="",
                        help='GitHub repository link (optional)')
    args = parser.parse_args()

    if not args.github_link == "":
        github_link = args.github_link

    app.run()
