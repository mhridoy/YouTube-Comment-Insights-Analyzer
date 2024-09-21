#clean_repo.py
import os
import subprocess
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Function to update the .gitignore file
def update_gitignore():
  gitignore_content = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Virtual environments
venv/
env/
.venv/
.env/

# Kaggle configuration files
.kaggle/

# Replit configuration files
.replit
replit.nix

# Dataset and large files
*.zip
*.tar.gz
*.rar
*.csv
*.xlsx

# Ignore archive files
archive.zip

# Other system files
.DS_Store
Thumbs.db

# Logs
*.log

# Node.js specific (if you have frontend code)
node_modules/

# Python poetry lock file
poetry.lock
"""
  try:
    logger.info("Updating .gitignore file...")
    with open('.gitignore', 'w') as gitignore_file:
      gitignore_file.write(gitignore_content)
    logger.info(".gitignore file updated successfully.")
  except Exception as e:
    logger.error(f"Failed to update .gitignore: {str(e)}")
    raise


# Function to run git commands
def run_git_command(command, description):
  try:
    logger.info(f"Running command: {' '.join(command)} ({description})")
    subprocess.run(command, check=True)
  except subprocess.CalledProcessError as e:
    logger.error(f"Failed to run command: {' '.join(command)} ({description})")
    logger.error(f"Error: {e}")
    raise
  except Exception as e:
    logger.error(f"An unexpected error occurred: {str(e)}")
    logger.error(traceback.format_exc())
    raise


# Function to remove previously tracked files that should now be ignored
def clean_git_repo():
  try:
    # Unstage all previously tracked files
    run_git_command(['git', 'rm', '-r', '--cached', '.'],
                    "Untracking all files")

    # Stage the changes (after updating .gitignore)
    run_git_command(['git', 'add', '.'],
                    "Staging all files except ignored ones")

    # Commit the changes
    run_git_command(
        ['git', 'commit', '-m', 'Clean repository based on .gitignore'],
        "Committing changes")
  except Exception as e:
    logger.error(f"An error occurred while cleaning the repository: {str(e)}")
    raise


# Function to push changes to GitHub
def push_changes(repo_url, token):
  try:
    # Ensure the GitHub remote URL uses the token for authentication
    auth_repo_url = f"https://x-access-token:{token}@{repo_url.split('https://')[1]}"

    # Push the changes to GitHub
    run_git_command(['git', 'push', auth_repo_url, 'main'],
                    "Pushing changes to GitHub")
    logger.info("Successfully pushed code to GitHub.")
  except Exception as e:
    logger.error(f"An error occurred while pushing changes: {str(e)}")
    raise


def main():
  # Repository details
  repo_url = "https://github.com/mhridoy/YouTube-Comment-Insights-Analyzer.git"
  token = os.getenv(
      'GITHUB_TOKEN')  # Ensure your token is in the environment variables

  if not token:
    logger.error("GitHub token not found in environment variables")
    raise Exception("GitHub token not found in environment variables")

  try:
    # Step 1: Update the .gitignore file
    update_gitignore()

    # Step 2: Clean the repository by untracking ignored files and committing changes
    clean_git_repo()

    # Step 3: Push the cleaned repository to GitHub
    push_changes(repo_url, token)

  except Exception as e:
    logger.error(f"An error occurred: {str(e)}")
    logger.error(traceback.format_exc())


if __name__ == "__main__":
  main()
