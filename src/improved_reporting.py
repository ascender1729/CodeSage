from jinja2 import Template

def generate_detailed_report(results):
    # Group issues by type
    grouped_issues = {}
    for file, issues in results.items():
        for issue in issues:
            if issue['type'] not in grouped_issues:
                grouped_issues[issue['type']] = []
            grouped_issues[issue['type']].append({**issue, 'file': file})

    # Generate HTML report
    template = Template('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CodeSage Detailed Report</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; }
            h1, h2 { color: #2c3e50; }
            .issue-type { margin-bottom: 30px; }
            .issue { margin-bottom: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; }
            .issue-file { font-weight: bold; color: #34495e; }
            .issue-message { color: #e74c3c; }
            .summary { margin-top: 30px; font-style: italic; }
        </style>
    </head>
    <body>
        <h1>CodeSage Detailed Report</h1>
        {% for issue_type, issues in grouped_issues.items() %}
        <div class="issue-type">
            <h2>{{ issue_type | replace("_", " ") | title }}</h2>
            {% for issue in issues %}
            <div class="issue">
                <span class="issue-file">{{ issue.file }}:{{ issue.line }}</span>
                <span class="issue-message">{{ issue.message }}</span>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
        <div class="summary">
            <p>Total issues found: {{ results | sum(attribute='__len__') }}</p>
        </div>
    </body>
    </html>
    ''')
    return template.render(grouped_issues=grouped_issues, results=results)