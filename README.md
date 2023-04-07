# 💻 ❓ GitHub Helper

GitHub Helper is a Python Flask application that leverages GPT-based language model to automatically respond to GitHub
issues and provide chat and Q&A functionality.

It allows users to interact with a chatbot or get answers to specific questions using a language model. The script clones a specified GitHub repository containing documentation, index data and initializes a chatbot or QA system based on the model.

It is built on [the Langchain library](https://github.com/hwchase17/langchain), which is built on top of GPT-based
language models, enabling efficient and advanced natural language processing capabilities.

## Features

* Clone and load a specified GitHub repository to use it as a local vector store, enabling search and retrieval of
  information from the repository content

* Automatically reply to newly opened GitHub issues using knowledge from repository

* Provides a simple web-based chat UI for user interaction and testing of the chatbot

* Supports Flask web framework for hosting the application

## Installation

### Docker

deploy the GitHub Helper using Docker:

1. Clone this repository:

`git clone https://github.com/nasirus/github_helper.git
cd langchain-github-helper`

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

### Install the required dependencies:

`pip install -r requirements.txt`

## Run the Flask application:

`python server.py`

## Usage

### GitHub Webhook

Configure your GitHub repository's webhook settings to point to your application's /github_webhook endpoint. For
example, https://yourdomain.com/github_webhook.
When a new issue is opened in the repository, the application will automatically reply with a response generated by the
GPT-based language model.

### Chat

http://127.0.0.1:5000/

This chat interface is a minimal web-based UI for interacting with the Langchain GitHub Helper. It displays the
conversation, has an input field for user messages, and a "Send" button. The interface is styled with an external CSS
file and uses JavaScript for interaction with the Flask backend.

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