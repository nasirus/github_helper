import os
import shutil
import stat

import git
import requests


def github_reply(repo_owner: str, repo_name: str, issue_number: str, comment_body: str):
    # get the value of the "GITHUB_TOKEN" environment variable
    access_token = os.environ['GITHUB_TOKEN']

    """
    Post a comment on a given GitHub issue.

    :param repo_owner: The owner of the repository.
    :param repo_name: The name of the repository.
    :param issue_number: The issue number to comment on.
    :param comment_body: The content of the comment.
    """
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments'
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github+json',
    }

    payload = {
        'body': comment_body.strip(),
    }

    response = None
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        print('Comment posted successfully.')
    except requests.exceptions.HTTPError as e:
        print(f'Failed to post comment. Status code: {response.status_code}. Error: {e}')


def get_issue_comments(repo_owner, repo_name, issue_number):
    access_token = os.getenv('GITHUB_TOKEN', "")
    assert access_token, "GITHUB_TOKEN environment variable is missing from .env"

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Error: Received status code {response.status_code} from GitHub API."

    comments_data = response.json()

    if isinstance(comments_data, dict):
        comments_data = [comments_data]
    elif not isinstance(comments_data, list):
        return ""

    return "\n".join([comment["body"] for comment in comments_data])


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_git_repo(github_link: str, reload: bool = False, root_dir: str = "data", root_db: str = "db") -> str:
    repo_name = github_link.rsplit('/', 1)[-1].split('.')[0]
    repo_path = os.path.join(root_dir, repo_name)
    db_path = os.path.join(root_db, repo_name)

    if reload:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, onerror=remove_readonly)
        if os.path.exists(db_path):
            shutil.rmtree(db_path, onerror=remove_readonly)

    if not os.path.exists(repo_path) and not os.path.exists(db_path):
        git.Repo.clone_from(github_link, repo_path)

    return repo_name


def get_github_link(args_github_link):
    if args_github_link:
        return args_github_link
    else:
        env_github_link = os.getenv('GITHUB_LINK', "")
        assert env_github_link, "GITHUB_LINK environment variable is missing from .env"

        if env_github_link:
            return env_github_link
        else:
            raise ValueError("GitHub link not provided in the command line or environment variables")
