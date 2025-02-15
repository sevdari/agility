import os
from dotenv import load_dotenv
from openai import OpenAI
import pathspec # For parsing .gitignore files

# Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# # Set OpenAI API key from environment variable
# openai_api_key = os.getenv("OPENAI_API_KEY")
# if not openai_api_key:
    # raise ValueError("OPENAI_API_KEY not found in the .env file. Please set it.")

def read_repository(repo_path, extensions=(".py", ".js", ".java", ".ts")):
    """
    Recursively reads files from the given repository path, excluding files and directories 
    that match the patterns in the .gitignore file, and concatenates their contents
    into a single string with file path headers. Only files with specified extensions are included.
    """
    # Load .gitignore patterns if available.
    gitignore_path = os.path.join(repo_path, ".gitignore")
    spec = None
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r", encoding="utf-8") as git_file:
                gitignore_lines = git_file.read().splitlines()
                spec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_lines)
        except Exception as e:
            print(f"Error reading .gitignore: {e}")

    content_list = []
    for dirpath, _, filenames in os.walk(repo_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            # Get the path relative to repo_path so we can match against .gitignore patterns
            relative_path = os.path.relpath(full_path, repo_path)

            # Exclude files that match .gitignore patterns if available.
            if spec and spec.match_file(relative_path):
                continue

            # Only include files with the specified extensions.
            if filename.endswith(extensions):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        file_contents = f.read()
                        # Append a header with the relative file path.
                        content_list.append(f"--- File: {relative_path} ---\n{file_contents}\n")
                except Exception as e:
                    print(f"Error reading {full_path}: {e}")
    return "\n".join(content_list)

def generate_issues(epic, repository_context):
    """
    Generate issues by sending the epic and the entire repository context to an LLM.
    The prompt instructs the LLM to break down the epic into a list of well-defined development issues.
    """
    prompt = f"""
You are a seasoned software project planner. Given the epic below and the complete context of the project's repository,
please break down the epic into a list of well-defined development issues. Each issue should include:
- A short title
- A detailed description explaining what needs to be done
- References to relevant parts of the repository (file paths or module names if appropriate)

Epic:
\"\"\"{epic}\"\"\"

Repository Context:
\"\"\"{repository_context}\"\"\"

Please list each issue in a structured format.
"""
    response = client.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an experienced project management assistant."},
        {"role": "user", "content": prompt},
    ],
    temperature=0.7)
    return response.choices[0].message.content

if __name__ == "__main__":
    repo_path = "/Users/aarjavjain/Desktop/Dev/aienginehackathon/agility"
    repository_context = read_repository(repo_path)

    # Example epic prompt
    epic = "Implement a feature that integrates user authentication with third-party OAuth."

    issues = generate_issues(epic, repository_context)
    print("Generated Issues:\n", issues) 