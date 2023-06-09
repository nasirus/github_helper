import hashlib
import hmac
import logging
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask import jsonify, render_template, make_response, abort

from github_helper import github_reply, clone_git_repo
from llmhelper import LangchainHelper

app = Flask(__name__)

load_dotenv()

github_link = os.getenv('GITHUB_LINK', "")
assert github_link, "GITHUB_LINK environment variable is missing from .env"

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(levelname)s %(message)s')

module_name = clone_git_repo(github_link, False)
langchain_helper = LangchainHelper(module_name=module_name)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/github_webhook', methods=['POST'])
def github_webhook():
    secret_key = os.getenv('GITHUB_WEBHOOK_SECRET', "")
    assert secret_key, "GITHUB_WEBHOOK_SECRET environment variable is missing from .env"

    webhook_secret = secret_key.encode()

    # Get the signature from the request headers
    signature = request.headers.get('X-Hub-Signature-256')

    if not signature:
        abort(400, 'Missing signature header')

    # Calculate the expected signature using the request payload and webhook secret
    expected_signature = 'sha256=' + hmac.new(webhook_secret, request.data, hashlib.sha256).hexdigest()

    # Verify the signature
    if not hmac.compare_digest(signature, expected_signature):
        abort(401, 'Invalid signature')

    data = request.get_json()

    # Check if the payload is for an issue event
    if not ('repository' in data and 'issue' in data and 'action' in data):
        return "Payload not related to issues, ignoring", 200

    repo_owner = data['repository']['owner']['login']
    repo_name = data['repository']['name']
    issue_number = data['issue']['number']
    issue_title = data['issue']['title']
    issue_state = data['issue']['state']

    if issue_state != 'closed':

        if data['action'] == 'opened':
            issue_comment = data['issue']['body']

            result = langchain_helper.assist_github_issue(issue_title=issue_title, issue_comment=issue_comment)
            logging.info(result[0]['text'])

            github_reply(repo_owner=repo_owner, repo_name=repo_name, issue_number=issue_number,
                         comment_body=result[0]['text'])

        elif data['action'] == 'created':
            issue_comment = data['comment']['body']

            if issue_comment and "@bothelper" in issue_comment:
                result = langchain_helper.assist_github_issue(issue_title=issue_title, issue_comment=issue_comment)
                logging.info(result[0]['text'])

                github_reply(repo_owner=repo_owner, repo_name=repo_name, issue_number=issue_number,
                             comment_body=result[0]['text'])

    return "OK", 200


@app.route('/chat', methods=['POST'])
def chat():
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
    data = request.get_json()
    question = data.get('question', '')
    result = langchain_helper.answer_simple_question(query=question)

    response = make_response(jsonify({"result": result}), 200)
    return response


@app.route('/')
def index():
    return render_template('index.html', module_name=module_name)


if __name__ == '__main__':
    app.run(debug=False)
