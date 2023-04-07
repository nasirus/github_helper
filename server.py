import argparse
import logging
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, make_response

from github_helper import github_reply, clone_git_repo
from llmhelper import LangchainHelper

app = Flask(__name__)
load_dotenv()
github_link = os.environ['GITHUB_LINK']

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(levelname)s %(message)s')

module_name = clone_git_repo(github_link, False)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/github_webhook', methods=['POST'])
def github_webhook():
    data = request.get_json()
    langchain_helper = LangchainHelper(module_name=module_name)

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
    langchain_helper = LangchainHelper(module_name=module_name)
    data = request.get_json()
    chat_history = data.get('chat_history', [])
    query = data.get('question', '')
    result = langchain_helper.initialize_chat_bot()({"question": query, "chat_history": chat_history})
    response = {
        "answer": result["answer"],
        "chat_history": chat_history + [(query, result["answer"])]
    }
    response = make_response(jsonify({"result": response}), 200)
    return response


@app.route('/qa', methods=['POST'])
def qa():
    langchain_helper = LangchainHelper(module_name=module_name)
    data = request.get_json()
    question = data.get('question', '')
    result = langchain_helper.answer_simple_question(query=question)

    response = make_response(jsonify({"result": result}), 200)
    return response


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

    app.run(debug=False)
