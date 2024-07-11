import os
import subprocess
from github import Github
from main import load_config
from enhanced_analysis import EnhancedCodeSage
from improved_reporting import generate_detailed_report

def analyze_github_pr(repo_owner, repo_name, pr_number, github_token):
    g = Github(github_token)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    pr = repo.get_pull(pr_number)

    # Clone the repository
    repo_dir = f"temp_{repo_name}"
    subprocess.run(["git", "clone", repo.clone_url, repo_dir])
    os.chdir(repo_dir)

    # Checkout the PR branch
    subprocess.run(["git", "fetch", "origin", f"pull/{pr_number}/head:pr_{pr_number}"])
    subprocess.run(["git", "checkout", f"pr_{pr_number}"])

    # Analyze changed files
    changed_files = pr.get_files()
    results = {}
    for file in changed_files:
        if file.filename.endswith('.py'):
            config = load_config('../config.yaml')
            sage = EnhancedCodeSage(config)
            issues = sage.analyze_file(file.filename)
            if issues:
                results[file.filename] = issues

    # Generate report
    report = generate_detailed_report(results)

    # Post report as a comment on the PR
    pr.create_issue_comment(f"CodeSage Analysis Results:\n\n```html\n{report}\n```")

    # Clean up
    os.chdir('..')
    subprocess.run(["rm", "-rf", repo_dir])

    return results