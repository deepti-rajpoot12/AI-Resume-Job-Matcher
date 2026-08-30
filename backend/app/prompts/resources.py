"""Trusted resource catalog. Only these URLs may be returned to clients."""

TRUSTED_RESOURCES = {
    "Python": [("Python Tutorial", "https://docs.python.org/3/tutorial/")],
    "Java": [("Dev.java Learn", "https://dev.java/learn/")],
    "JavaScript": [("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide")],
    "TypeScript": [("TypeScript Handbook", "https://www.typescriptlang.org/docs/handbook/intro.html")],
    "React": [("React Learn", "https://react.dev/learn")],
    "Angular": [("Angular Documentation", "https://angular.dev/overview")],
    "SQL": [("PostgreSQL Tutorial", "https://www.postgresql.org/docs/current/tutorial.html")],
    "Docker": [("Docker Get Started", "https://docs.docker.com/get-started/")],
    "Kubernetes": [("Kubernetes Basics", "https://kubernetes.io/docs/tutorials/kubernetes-basics/")],
    "AWS": [("AWS Getting Started", "https://aws.amazon.com/getting-started/")],
    "Azure": [("Microsoft Learn Azure", "https://learn.microsoft.com/training/azure/")],
    "GCP": [("Google Cloud Skills Boost", "https://www.cloudskillsboost.google/")],
    "Git": [("Pro Git Book", "https://git-scm.com/book/en/v2")],
}


def resources_for_skills(skills: list[str]) -> str:
    lines: list[str] = []
    for skill in skills:
        for known_skill, resources in TRUSTED_RESOURCES.items():
            if known_skill.lower() in skill.lower():
                for title, url in resources:
                    lines.append(f"Skill: {known_skill} | Resource: {title} | URL: {url}")
    return "\n".join(dict.fromkeys(lines)) or "No trusted resource URL is available for these gaps."


def trusted_url(url: str) -> bool:
    return any(url == known_url for resources in TRUSTED_RESOURCES.values() for _, known_url in resources)
