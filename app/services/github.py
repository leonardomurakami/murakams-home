import httpx
from typing import List, Dict, Optional
from ..config import settings


class GitHubService:
    """Service for fetching GitHub repository data"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.username = settings.github_username
        self.token = settings.github_token
    
    async def get_repositories(self, limit: int = 10) -> List[Dict]:
        """Fetch public repositories from GitHub"""
        if not self.username:
            return []
        
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/users/{self.username}/repos",
                    headers=headers,
                    params={
                        "sort": "updated",
                        "direction": "desc",
                        "per_page": limit,
                        "type": "public"
                    }
                )
                response.raise_for_status()
                
                repos = response.json()
                
                # Transform to our format
                formatted_repos = []
                for repo in repos:
                    # Skip forks unless you want them
                    if repo.get("fork", False):
                        continue
                    
                    formatted_repo = {
                        "name": repo["name"],
                        "description": repo.get("description", ""),
                        "github_url": repo["html_url"],
                        "demo_url": repo.get("homepage") if repo.get("homepage") else None,
                        "technologies": self._extract_technologies(repo),
                        "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language", ""),
                        "updated_at": repo.get("updated_at", ""),
                        "source": "github"
                    }
                    formatted_repos.append(formatted_repo)
                
                return formatted_repos
                
        except Exception as e:
            print(f"Error fetching GitHub repositories: {e}")
            return []
    
    def _extract_technologies(self, repo: Dict) -> str:
        """Extract technologies from repository data"""
        techs = []
        
        # Add primary language
        if repo.get("language"):
            techs.append(repo["language"])
        
        # You could extend this to fetch languages from the languages API
        # or parse topics if available
        if repo.get("topics"):
            techs.extend(repo["topics"])
        
        return ", ".join(techs)
    
    async def get_repository_languages(self, repo_name: str) -> Optional[Dict]:
        """Fetch languages used in a specific repository"""
        if not self.username:
            return None
        
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{self.username}/{repo_name}/languages",
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            print(f"Error fetching repository languages: {e}")
            return None
