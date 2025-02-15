import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_github_issue(title, body, repo_owner, repo_name):
    """
    Create a new GitHub issue
    
    Args:
        title (str): Issue title
        body (str): Issue description
        repo_owner (str): Repository owner/organization
        repo_name (str): Repository name
    
    Returns:
        dict: Response from GitHub API
    """
    # GitHub API endpoint
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    
    # Get GitHub token from environment variable
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in .env file")
    
    # Headers for authentication
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Issue data
    data = {
        'title': title,
        'body': body
    }
    
    # Create the issue
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Issue created successfully! URL: {response.json()['html_url']}")
        return response.json()
    else:
        print(f"Failed to create issue. Status code: {response.status_code}")
        print(f"Error message: {response.text}")
        return None

if __name__ == "__main__":
    # Example usage
    owner = "sevdari"  # Replace with repository owner
    repo = "agility"       # Replace with repository name
    
    issue_title = "Test Issue"
    issue_body = """
    This is a test issue created via the GitHub API.
    
    ## Details
    - Created automatically
    - Using Python script
    """
    
    create_github_issue(issue_title, issue_body, owner, repo)
