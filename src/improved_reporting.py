from jinja2 import Template

def generate_detailed_report(results):
    grouped_issues = {}
    total_issues = 0
    for file, issues in results.items():
        total_issues += len(issues)
        for issue in issues:
            if issue['type'] not in grouped_issues:
                grouped_issues[issue['type']] = []
            grouped_issues[issue['type']].append({**issue, 'file': file})

    template = Template('''
    <h2>CodeSage Detailed Report</h2>
    {% for issue_type, issues in grouped_issues.items() %}
    <h3 class="issue-type">{{ issue_type | replace("_", " ") | title }}</h3>
    {% for issue in issues %}
    <div class="issue">
        <strong>{{ issue.file }}:{{ issue.line }}</strong> {{ issue.message }}
    </div>
    {% endfor %}
    {% endfor %}
    <p><em>Total issues found: {{ total_issues }}</em></p>
    ''')
    
    return template.render(grouped_issues=grouped_issues, total_issues=total_issues)