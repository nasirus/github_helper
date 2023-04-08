[![Build Az](https://github.com/nasirus/github_helper/actions/workflows/main_nasirus-github-helper.yml/badge.svg)](https://github.com/nasirus/github_helper/actions/workflows/main_nasirus-github-helper.yml)

# 💻 ❓ GitHub Helper

GitHub Helper is a Python application that leverages GPT-based language model to automatically respond to GitHub
issues and provide chat and Q&A functionality.

It allows users to interact with a chatbot or get answers to specific questions using a language model. The script
clones a specified GitHub repository containing documentation, index data and initializes a chatbot or QA system based
on the model.

It is built on [the Langchain library](https://github.com/hwchase17/langchain), which is built on top of GPT-based
language models, enabling efficient and advanced natural language processing capabilities.

## Features

* Clone and load a specified GitHub repository to use it as a local vector store, enabling search and retrieval of
  information from the repository content

* Automatically reply to newly opened GitHub issues using knowledge from repository

* Provides a simple web-based chat UI for user interaction and testing of the chatbot

* Provides a command line for interacting

## Installation

### Docker

deploy the GitHub Helper using Docker:

1. Clone this repository:

`git clone https://github.com/nasirus/github_helper.git
cd github-helper`

2. Set the required environment variables:

`cp .env.example .env`

Edit the .env file and set the GITHUB_LINK environment variable with the GitHub repository link and OPENAI_API_KEY

`GITHUB_LINK=https://github.com/yoheinakajima/babyagi.git`
`OPENAI_API_KEY=`

3. Build the Docker image:

`docker build -t github-helper .`

4. Run the Docker container:

`docker run -d -p 5000:5000 --name github-helper --env-file .env github-helper`

Once the container is running, you can access the application at http://127.0.0.1:5000.

## How to run manually

1. Clone this repository:

`git clone https://github.com/nasirus/github_helper.git
cd github-helper`

2. Install the required dependencies:

`pip install -r requirements.txt`

## 1 - Run the Flask application:

`python server.py`

## 2 - Run console chat:

`python main.py`

## Usage

### GitHub Webhook Functionality for Your Repository

In your repo, the GitHub webhook functionality is used to automatically respond to new issues opened in the specified
repository. When a new issue is opened, your app will analyze the issue title and body, generate a helpful response
using the LangchainHelper module, and post that response as a comment on the issue.

#### Key Components

* Route: The /github_webhook route is used to receive webhook events from GitHub.

* Event handling: The webhook handler processes the opened event, which is triggered when a new issue is created.

* Issue analysis: The issue title and body are passed to the assist_github_issue function of the LangchainHelper module
  to generate a helpful response.

* Comment posting: The generated response is posted as a comment on the issue using the github_reply function.

#### Usage

To use the GitHub webhook functionality in your app, follow these steps:

1. Set up a webhook in your GitHub repository:

* Go to the repository settings on GitHub.
* Click on "Webhooks" in the left sidebar.
* Click "Add webhook."
* Enter your app's URL followed by /github_webhook in the "Payload URL" field (
  e.g., https://yourappdomain.com/github_webhook).
* Select "application/json" as the "Content type."
* Choose the "Let me select individual events" option and check the "Issues" event.
* Click "Add webhook" to save your settings.

2. Ensure that the GITHUB_LINK environment variable is set to the repository URL in your .env file.

3. Run your app and ensure that the webhook route (/github_webhook) is accessible from the internet.

Once the webhook is set up and your app is running, new issues created in the repository will trigger the webhook, and
your app will automatically generate and post responses as comments on the issues.

### Web Chat Interface

http://127.0.0.1:5000/

This chat interface is a minimal web-based UI for interacting with the Langchain GitHub Helper. It displays the
conversation, has an input field for user messages, and a "Send" button. The interface is styled with an external CSS
file and uses JavaScript for interaction with the Flask backend.

### Command Line Chat Interface

The Command Line Chat Interface provides an interactive way for users to communicate with the Github Helper module
directly from the console.

#### Features

* Two modes of operation: The chat interface offers two modes, "chat" and "qa". In "chat" mode, users can have an
  ongoing conversation with the Github Helper module. In "qa" mode, users can ask a single question and receive an
  answer.

* Chat history: The chat interface maintains a history of messages and responses, allowing users to review previous
  interactions.

#### Usage

`python main.py --bot_mode chat --github_link https://github.com/user/repo.git`

* --bot_mode: Choose the mode for the bot: 'chat' or 'qa'. Default is 'chat'.
* --github_link: The GitHub link for the repository to clone. Default is 'https://github.com/nasirus/github_helper.git'.
* --question: The question to be answered in 'qa' mode. Default is 'what is github helper?'.

For 'qa' mode, use the following command:

`python main.py --bot_mode qa --github_link https://github.com/user/repo.git --question "What is the main function of the project?"`

### Q&A

Send a POST request to the /qa endpoint with the following JSON payload:

`curl -X POST -H "Content-Type: application/json" -d '{"question": "your_question_here"}' http://127.0.0.1:5000/qa
`

`{
"question": "your_question_here"
}`

The response will include the generated answer:

`{
"result": "generated_answer_here"
}`

## License

This project is licensed under the MIT License. See the LICENSE file for details.