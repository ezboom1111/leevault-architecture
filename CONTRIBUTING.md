# Contributing

Contributions should improve the generic architecture without introducing real
operational data.

Before opening a pull request:

1. keep examples synthetic and organization-neutral;
2. do not paste logs, prompts, database extracts, credentials, or local paths;
3. run `python -m unittest discover -s tests -v`;
4. run `python scripts/validate_public_repo.py .`;
5. explain which architectural contract changes and how it would be evaluated.

Security-sensitive findings should be described without including a live secret
or private reproduction corpus in the issue.
