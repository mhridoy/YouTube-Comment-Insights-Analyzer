import os
import subprocess
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_git_command(command, description):
    """Utility function to run git commands."""
    try:
        logger.info(f"Running command: {' '.join(command)} ({description})")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to run command: {' '.join(command)} ({description})")
        logger.error(f"Error: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        raise


def push_code_to_github(repo_url, token):
    """Push the updated code to the GitHub repository."""
    try:
        # Ensure the GitHub remote URL uses the token for authentication
        auth_repo_url = f"https://x-access-token:{token}@{repo_url.split('https://')[1]}"

        # Add all changes to git
        run_git_command(['git', 'add', '.'], "Staging all changes")

        # Commit the changes
        run_git_command(['git', 'commit', '-m', 'Update project files'],
                        "Committing changes")

        # Push the changes to GitHub using token-authenticated URL
        run_git_command(['git', 'push', auth_repo_url, 'main'],
                        "Pushing changes to GitHub")

        logger.info("Successfully pushed code to GitHub")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())


def main():
    # Repository details
    repo_url = "https://github.com/mhridoy/YouTube-Comment-Insights-Analyzer.git"
    token = os.getenv(
        'GITHUB_TOKEN')  # Ensure your token is in the environment variables

    if not token:
        logger.error("GitHub token not found in environment variables")
        raise Exception("GitHub token not found in environment variables")

    try:
        # Push code to GitHub
        push_code_to_github(repo_url, token)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
