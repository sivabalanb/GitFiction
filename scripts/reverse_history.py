import os
import requests

# Get GitHub username from GitHub Actions input
USERNAME = os.getenv("GITHUB_USERNAME", "octocat")  # Default to 'octocat'

# Get user's repositories
repos_url = f"https://api.github.com/users/{USERNAME}/repos"
repos_response = requests.get(repos_url)
repos = repos_response.json()

if repos_response.status_code != 200 or not repos:
    print("❌ Error fetching repositories for user:", USERNAME)
    exit(1)

# Pick the most starred repo (or first one)
repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
REPO = repos[0]["name"]

# Fetch commits
API_URL = f"https://api.github.com/repos/{USERNAME}/{REPO}/commits"
response = requests.get(API_URL)
commits = response.json()

if response.status_code != 200 or not commits:
    print(f"❌ No commits found for {USERNAME}/{REPO}")
    exit(1)

# Extract commit messages and dates
commit_history = [
    {"message": c["commit"]["message"], "date": c["commit"]["author"]["date"]}
    for c in commits
]

# Reverse commit order
commit_history.reverse()

# Format into Markdown
output = f"# 🔄 Alternate GitHub History for {USERNAME} (Repo: {REPO})\n\n"
for commit in commit_history:
    output += f"- **{commit['date']}** → {commit['message']}\n"

# Save to file
filename = f"reverse_history_{USERNAME}.md"
with open(filename, "w") as f:
    f.write(output)

print(f"✅ Reordered commit history saved to {filename}")
