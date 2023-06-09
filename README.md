[![Build Az](https://github.com/nasirus/github_helper/actions/workflows/main_nasirus-github-helper.yml/badge.svg)](https://github.com/nasirus/github_helper/actions/workflows/main_nasirus-github-helper.yml)
[![Open in Codespaces](https://img.shields.io/badge/Open%20in-Codespaces-blue?logo=github)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=624546212&machine=basicLinux32gb&location=EastUs)

# 💻 ❓ GitHub Helper

Are you looking to ask questions about your favorite repository? 

Do you want to integrate a helper for your issue management? 

You've come to the right place!

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

* Reply to Issue Comments with Mention "@bothelper"

* Provides a simple web-based chat UI for user interaction and testing of the chatbot

* Provides a command line for interacting

## Installation

### Docker

deploy the GitHub Helper using Docker:

1. Clone this repository:

    `git clone https://github.com/nasirus/github_helper.git`
    
    `cd github_helper`

2. Set the required environment variables:
    
    `cp .env.example .env`
    
    Edit the .env file and set the GITHUB_LINK environment variable with the GitHub repository link and OPENAI_API_KEY
    
    `FLASK_DEBUG=False`
    
    `GITHUB_LINK=https://github.com/nasirus/github_helper`
    
    `OPENAI_API_KEY=`

    `OPENAI_API_BASE=`
    
    `OPENAI_API_TYPE=azure`

    `GITHUB_TOKEN=`

     [creating-a-personal-access-token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
    
    `GITHUB_WEBHOOK_SECRET=`

    Generate a random secret

    NB:

   - This example uses Azure OpenAI LLM by default. If you want to use another LLM, you can set up any [Langchain model](https://python.langchain.com/en/latest/modules/models/llms/integrations.html) in [this file](https://github.com/nasirus/github_helper/blob/main/llmhelper.py#L12) .

   - `GITHUB_TOKEN` and `GITHUB_WEBHOOK_SECRET` are required only if you want to set up auto-reply in issues.

   - `OPENAI_API_BASE` and `OPENAI_API_TYPE` are required only if you use AzureOpenAI

3. Build the Docker image:

    `docker build -t github-helper .`

4. Run the Docker container:

    `docker run -d -p 5000:5000 --name github-helper --env-file .env github-helper`
    
    Once the container is running, you can access the application at http://localhost:5000/.

## How to run manually

1. Clone this repository:

    `git clone https://github.com/nasirus/github_helper.git`
    
    `cd github_helper`

2. [Set the required environment variables:](#Docker)

3. Create a virtual environment.

    `python -m venv myvenv`

4. To activate the virtual environment, use the appropriate command for your operating system:

    . For Windows:

    myvenv\Scripts\activate.bat
  
    . For macOS and Linux:
  
    source myvenv/bin/activate

5. Install the required dependencies:

    `pip install -r requirements.txt`

### a - Run the Flask application (For chat UI):

The GitHub repository used by default is the value defined in .env file "`GITHUB_LINK=`"

`python server.py`

you can access the application at http://127.0.0.1:5000.

### b - Run console chat (Command line for interacting):

`python main.py`

GitHub Helper provides a chatbot or a simple question-answering bot utilizing
OpenAI's GPT-based language models. The script allows users to switch between two modes: chat mode for a more
interactive conversation and QA mode for quick one-time question-answering.

`python main.py [--bot_mode <mode>] [--github_link <link>] [--question <question>]`

* --bot_mode: Specify the mode for the bot, either chat or qa. Defaults to chat.
* --github_link: Provide the GitHub repository link (optional).
* --question: The question to be answered in 'qa' mode. Defaults to "what is github helper?".
* --reload: Reload the git repository if it already exists locally. This option is not required; include it only if you want to force the repository to reload.

Example :

`python main.py --github_link https://github.com/nasirus/github_helper --bot_mode chat`

`python main.py --github_link https://github.com/nasirus/github_helper --bot_mode qa --question "What is github helper ?"`

## Usage

### GitHub Webhook Functionality for Your Repository

The GitHub webhook functionality is used to automatically respond to new issues opened in the specified
repository. When a new issue is opened, your bot will analyze the issue title and body, generate a helpful response
using the LangchainHelper module, and post that response as a comment on the issue.

#### Key Components

* Route: The /github_webhook route is used to receive webhook events from Github.

* Event handling: The webhook handler processes the opened event, which is triggered when a new issue is created.

* Issue analysis: The issue title and body are passed to the assist_github_issue function of the LangchainHelper module
  to generate a helpful response.

* Comment posting: The generated response is posted as a comment on the issue using the github_reply function.

* Security : allows you to receive and process GitHub webhooks while ensuring the authenticity of incoming requests by
  verifying the secret key.

### Reply to Issue Comments with Mention

The GitHub Helper Bot can reply to issue comments when specifically mentioned using "@bothelper" in the comment. This
feature allows the bot to listen for new issue comments and respond when the bot is mentioned.

To use this feature, simply mention "@bothelper" in your issue comment when you want the bot to respond to it. This
helps in reducing the noise in the issue thread, as the bot will only reply when explicitly mentioned.

#### How to set up GitHub Webhook

To use the GitHub webhook functionality in your repository, follow these steps:

1. Set up a webhook in your GitHub repository:

   * Go to the repository settings on GitHub.
   * Click on "Webhooks" in the left sidebar.
   * Click "Add webhook."
   * Enter your app's URL followed by /github_webhook in the "Payload URL" field (
     e.g., https://yourappdomain.com/github_webhook).
   * Select "application/json" as the "Content type."
   * Choose the "Let me select individual events" option and check the "Issues" and "Issue comments" event.
   * Enter your Secret (Must be the same as defined in .env file `GITHUB_WEBHOOK_SECRET`)
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

### Command Line

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
* --reload: Reload the git repository if it already exists locally. This option is not required; include it only if you want to force the repository to reload.

For 'qa' mode, use the following command:

`python main.py --bot_mode qa --github_link https://github.com/user/repo.git --question "What is the main function of the project?"`

### Q&A Endpoint

Send a POST request to the /qa endpoint with the following JSON payload:

`curl -X POST -H "Content-Type: application/json" -d '{"question": "your_question_here"}' http://127.0.0.1:5000/qa
`

The response will include the generated answer:

`{
"result": "generated_answer_here"
}`

## Example 
### QA

There is some pretrained index ,so you can start asking your questions without indexing data :

`python main.py --github_link https://github.com/nomic-ai/gpt4all --bot_mode qa --question "What is gpt4all ?"`

`python main.py --github_link https://github.com/Torantulino/Auto-GPT --bot_mode qa --question "What is Auto-GPT?"`

`python main.py --github_link https://github.com/microsoft/JARVIS --bot_mode qa --question "What is JARVIS?"`

`python main.py --github_link https://github.com/hwchase17/langchain --bot_mode qa --question "which llm support streaming?"`

You can find all pretrained index in "db" folder

### Chat

`python main.py --github_link https://github.com/hwchase17/langchain --bot_mode chat`

### Chat UI

![Chat Interface Example](/static/ChatInterfaceExample.png)

### Automatically reply to newly opened GitHub issues

[Real issue on Langchain fork](https://github.com/nasirus/langchain/issues) 

[Real issue on llama_index fork](https://github.com/nasirus/llama_index/issues)

### Try auto reply with local server :

* Download ngrok for your platform at https://ngrok.com/download and unzip the file.
* Open a terminal/command prompt in the ngrok folder.
* Start your local web server on 5000 port ([server.py](https://github.com/nasirus/github_helper/blob/main/server.py)).
* Run ./ngrok http 5000 in the terminal/command prompt to create a tunnel.
* Copy the generated public URL and [follow those steps:](#how-to-set-up-github-webhook)

## License

This project is licensed under the MIT License. See the LICENSE file for details.
