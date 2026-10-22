import requests


def get_repo_stars(owner: str, repo: str) -> int:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["stargazers_count"]


if __name__ == "__main__":
    stars = get_repo_stars("microsoft", "agent-framework")
    print(f"Microsoft Agent Framework has {stars:,} stars")