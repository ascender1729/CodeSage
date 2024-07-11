import os
import subprocess
from github import Github
from main import CodeSage, load_config

def get_changed_files(base_branch, head_branch):
    """Get the list of changed files between two branches."""
    cmd = f"git diff --name-only {base_branch}..{head_branch}"
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return [file for file in result.stdout.split('\n') if file.endswith('.py')]

def analyze_pr(repo_path, base_branch, head_branch, github_token, repo_name, pr_number):
    """Analyze the changes in a pull request."""
    os.chdir(repo_path)
    
    config = load_config('config.yaml')
    sage = CodeSage(config)
    
    changed_files = get_changed_files(base_branch, head_branch)
    results = {}
    
    for file_path in changed_files:
        issues = sage.analyze_file(file_path)
        if issues:
            results[file_path] = issues
    
    # Post results to GitHub
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    pull_request = repo.get_pull(pr_number)
    
    comment = "CodeSage Analysis Results:\n\n"
    for file_path, issues in results.items():
        comment += f"**{file_path}**\n"
        for issue in issues:
            comment += f"- Line {issue['line']}: [{issue['type']}] {issue['message']}\n"
        comment += "\n"
    
    pull_request.create_issue_comment(comment)

if __name__ == "__main__":
    # This could be called by a CI/CD pipeline
    repo_path = os.environ.get('REPO_PATH')
    base_branch = os.environ.get('BASE_BRANCH', 'main')
    head_branch = os.environ.get('HEAD_BRANCH')
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_name = os.environ.get('REPO_NAME')
    pr_number = int(os.environ.get('PR_NUMBER'))
    
    analyze_pr(repo_path, base_branch, head_branch, github_token, repo_name, pr_number)