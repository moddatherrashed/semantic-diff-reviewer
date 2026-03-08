# Semantic Diff Reviewer

Semantic Diff Reviewer is an AI-powered code review assistant for GitHub Pull Requests.  
Instead of only checking line-by-line changes, it analyzes modified functions, traces dependency impact, and uses an LLM to identify architectural risks, hidden regressions, and potential breaking changes.  
It then posts intelligent feedback directly on the Pull Request.

Repository: https://github.com/moddatherrashed/semantic-diff-reviewer

## Features

- **Semantic PR analysis** beyond textual diffs
- **Function-level change extraction** from modified files
- **Dependency-aware risk detection** across modules
- **LLM-powered review insights** for architecture and maintainability
- **Automated GitHub PR feedback** via comments/review threads
- **Webhook-driven workflow** for near real-time analysis
- **Optional AST parsing** with Tree-sitter for more accurate code understanding
- **Optional dependency graphing** with Neo4j for advanced impact analysis

## Tech Stack

- **Language:** Python
- **Web API:** FastAPI
- **GitHub Integration:** PyGithub + GitHub Webhooks
- **AI Provider:** OpenAI API
- **Optional Parsing:** Tree-sitter (AST-level function extraction)
- **Optional Graph Layer:** Neo4j (cross-module dependency graph)

## Project Structure

```text
semantic-diff-reviewer/
├── main.py           # FastAPI entrypoint + webhook endpoint(s)
├── github_api.py     # GitHub API utilities (PR metadata, comments, etc.)
├── parser.py         # Diff/function parsing logic
├── graph.py          # Dependency graph logic (optional Neo4j integration)
├── reviewer.py       # LLM prompting + review generation pipeline
├── requirements.txt  # Python dependencies
└── README.md
```

## How It Works

1. **GitHub sends a webhook** when a PR event occurs (opened, synchronized, reopened).
2. **FastAPI receives the event** and validates the webhook signature.
3. **PR diff is fetched** using GitHub APIs.
4. **Modified functions are extracted** from changed files (with optional AST support).
5. **Dependency impact is analyzed** to detect ripple effects between modules.
6. **LLM evaluates semantic risk** (breaking changes, architectural issues, missing tests, etc.).
7. **Automated feedback is posted** back to the PR as intelligent review comments.

## Installation

### 1) Clone the repository

```bash
git clone https://github.com/moddatherrashed/semantic-diff-reviewer.git
cd semantic-diff-reviewer
```

### 2) Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) (Optional) Install Tree-sitter and Neo4j drivers

Install only if you plan to use AST parsing and graph analysis enhancements.

## Environment Variables

Create a `.env` file in the project root:

```env
# Required
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_WEBHOOK_SECRET=your_webhook_secret
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

# Optional
OPENAI_MODEL=gpt-4o-mini
ENABLE_TREE_SITTER=false
ENABLE_NEO4J=false
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
LOG_LEVEL=INFO
```

Suggested variable reference:

| Variable | Required | Description |
| --- | --- | --- |
| `GITHUB_TOKEN` | Yes | Token used to fetch PR data and post review comments |
| `GITHUB_WEBHOOK_SECRET` | Yes | Secret for validating incoming GitHub webhook payloads |
| `OPENAI_API_KEY` | Yes | API key for LLM analysis |
| `OPENAI_MODEL` | No | Model name for review generation |
| `ENABLE_TREE_SITTER` | No | Toggle AST-based parsing |
| `ENABLE_NEO4J` | No | Toggle graph-based dependency analysis |
| `NEO4J_URI` | No | Neo4j connection URI |
| `NEO4J_USER` | No | Neo4j username |
| `NEO4J_PASSWORD` | No | Neo4j password |
| `LOG_LEVEL` | No | Logging verbosity |

## Running the Server

Start the FastAPI app locally:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

If needed, expose your local server for webhook delivery (for example using ngrok):

```bash
ngrok http 8000
```

Use the generated public URL as your webhook target.

## Setting Up GitHub Webhooks

1. Open your GitHub repository (`moddatherrashed/semantic-diff-reviewer`).
2. Go to **Settings -> Webhooks -> Add webhook**.
3. Configure:
   - **Payload URL:** `https://<your-public-url>/webhook`
   - **Content type:** `application/json`
   - **Secret:** same value as `GITHUB_WEBHOOK_SECRET`
   - **Events:** select **Pull requests** (and optionally **Pull request reviews**)
4. Save and trigger a PR update (push new commits) to test the pipeline.
5. Verify deliveries in **Settings -> Webhooks -> Recent Deliveries**.

## Example Output

Example of automated feedback posted to a PR:

```markdown
### Semantic Diff Review

**Risk Level:** High

- Function `process_invoice()` now returns `None` in one branch, but callers still expect a dict.
- `billing/service.py` introduced a dependency on `user/cache.py`, creating a potential circular import path.
- Breaking behavior detected: validation no longer enforces `currency_code`.

**Recommendations**
1. Restore a consistent return type in `process_invoice()`.
2. Move cache access behind an interface in `billing/adapters.py`.
3. Add regression tests for invoice validation and invalid currency paths.
```

## Future Improvements

- Inline code suggestions for safe refactoring
- Support for multi-language repositories with parser plugins
- Historical PR learning to reduce false positives
- Team-specific review policies and rule packs
- Confidence scoring and explainability for each finding
- Slack/Teams notifications for high-risk changes

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/semantic-check`)
3. Commit your changes (`git commit -m "Add semantic review enhancement"`)
4. Push your branch (`git push origin feat/semantic-check`)
5. Open a Pull Request

Please include tests and clear context in your PR description.

## License

This project is licensed under the MIT License.  
Add a `LICENSE` file if one is not already present.

