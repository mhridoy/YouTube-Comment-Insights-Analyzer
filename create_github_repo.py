import os
import requests
import subprocess
import traceback
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_github_repo(repo_name, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': repo_name,
        'private': False,  # Set to True if you want a private repository
    }
    response = requests.post('https://api.github.com/user/repos', headers=headers, json=data)

    if response.status_code == 201:
        logger.info(f"Repository '{repo_name}' created successfully.")
        return response.json()
    elif response.status_code == 422:
        logger.info(f"Repository '{repo_name}' already exists.")
        return get_github_repo(repo_name, token)  # Repo already exists, return its details
    else:
        logger.error(f"Failed to create repository: {response.status_code}, {response.text}")
        raise Exception("Failed to create repository.")

def get_github_repo(repo_name, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(f'https://api.github.com/repos/mhridoy/{repo_name}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_initial_commit():
    try:
        with open('README.md', 'w') as f:
            f.write("# YouTube Comment Insights Analyzer\n\nThis project analyzes YouTube comments using AI and provides insights.")

        subprocess.run(['git', 'add', 'README.md'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        logger.info("Created initial commit with README.md")
    except Exception as e:
        logger.error(f"Error creating initial commit: {str(e)}")
        raise

def push_changes(repo_url, token):
    try:
        logger.info("Adding all files to git")
        subprocess.run(['git', 'add', '.'], check=True)

        logger.info("Committing changes")
        subprocess.run(['git', 'commit', '-m', 'Update project files'], check=True)

        logger.info("Pushing to remote repository")
        subprocess.run(['git', 'push', '-u', f'https://x-access-token:{token}@github.com/mhridoy/YouTube-Comment-Insights-Analyzer.git', 'main'], check=True)

        logger.info("Successfully pushed changes to remote repository")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error in git operations: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def initialize_repo(repo_url, token):
    try:
        logger.info("Initializing git repository")
        subprocess.run(['git', 'init'], check=True)

        logger.info("Adding remote repository")
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)

        logger.info("Creating initial commit")
        create_initial_commit()

        logger.info("Pushing initial commit")
        subprocess.run(['git', 'push', '-u', f'https://x-access-token:{token}@github.com/mhridoy/YouTube-Comment-Insights-Analyzer.git', 'main'], check=True)

        # Now add all other files and push them
        logger.info("Adding all project files")
        subprocess.run(['git', 'add', '.'], check=True)

        logger.info("Committing all project files")
        subprocess.run(['git', 'commit', '-m', 'Add all project files'], check=True)

        logger.info("Pushing all files to GitHub")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)

    except subprocess.CalledProcessError as e:
        logger.error(f"Error in git operations: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        raise

def main():
    repo_name = 'YouTube-Comment-Insights-Analyzer'
    token = os.environ.get('GITHUB_TOKEN')

    if not token:
        logger.error("GitHub token not found in environment variables")
        raise Exception("GitHub token not found in environment variables")

    try:
        # Configure git user
        subprocess.run(['git', 'config', '--global', 'user.email', '17101016@uap-bd.edu'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.name', 'mhridoy'], check=True)
        logger.info("Configured git user")

        repo_data = get_github_repo(repo_name, token)
        if repo_data:
            logger.info(f"Repository exists: {repo_data['clone_url']}")
            push_changes(repo_data['clone_url'], token)
        else:
            logger.info(f"Repository does not exist. Creating {repo_name}")
            repo_data = create_github_repo(repo_name, token)
            initialize_repo(repo_data['clone_url'], token)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()
