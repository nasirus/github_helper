import argparse
import hashlib
import hmac
import logging
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, make_response, abort

from github_helper import github_reply, clone_git_repo, get_issue_comments, get_github_link
from llmhelper import LangchainHelper

app = Flask(__name__)
load_dotenv()
github_link = os.environ['GITHUB_LINK']
secret_key = os.environ.get('GITHUB_WEBHOOK_SECRET')
logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(levelname)s %(message)s')


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/github_webhook', methods=['POST'])
def github_webhook():
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
                previous_comments = get_issue_comments(repo_owner, repo_name, issue_number)
                issue_comment = previous_comments

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
    parser = argparse.ArgumentParser(description='CLI for Langchain script')
    parser.add_argument('--github_link', type=str, required=False,
                        help='GitHub repository link (optional)')
    parser.add_argument('--reload', action='store_true',
                        help='Reload the git repository if set, otherwise use existing one')
    args = parser.parse_args()

    github_link = get_github_link(args.github_link)
    module_name = clone_git_repo(github_link, args.reload)
    langchain_helper = LangchainHelper(module_name=module_name)

    app.run(debug=False)
