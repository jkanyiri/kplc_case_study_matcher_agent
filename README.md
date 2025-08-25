# 📚 Case Study Matcher Agent

An intelligent agent that helps find relevant case studies for your projects by analyzing project titles, problem statements, and proposed solutions. The agent uses LangGraph to orchestrate a workflow that generates optimized search queries and retrieves relevant case studies from the web.

## 🎯 What It Does

The Case Study Matcher Agent:
1. **Analyzes Project Context**: Takes your project title, problem statement, and proposed solution
2. **Generates Smart Queries**: Uses AI to create optimized search queries for finding relevant case studies
3. **Searches the Web**: Leverages Tavily Search to find up to 20 relevant case studies
4. **Returns Results**: Provides you with a curated list of case studies that match your project needs

## 🏗️ Architecture

Built with LangGraph, the agent follows a simple but effective workflow:
- **Generate Query Node**: AI-powered query generation based on project context
- **Search Case Studies Node**: Web search using Tavily Search API
- **State Management**: Tracks project details, generated queries, and search results

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- An OpenAI API Key and (optionally) a LangSmith API Key
- A Tavily Search API Key

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root with the following keys:

```dotenv
# Required APIs
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
LANGSMITH_API_KEY=your_langsmith_key

# LangChain
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=case_study_matcher

# Database (Docker Compose sets this automatically to PostgreSQL)
# DATABASE_URI=sqlite:///./langgraph.db

# Optional: Override default search parameters
# TAVILY_MAX_RESULTS=20
```

Notes:
- `OPENAI_API_KEY` is required for the agent to generate intelligent search queries
- `TAVILY_API_KEY` is required for web search functionality
- `LANGSMITH_API_KEY` is optional, only needed if you want tracing to LangSmith
- `DATABASE_URI` is automatically set by Docker Compose to PostgreSQL
- Redis and Postgres connection strings are provided by Docker Compose
- The agent will search for up to 20 case studies by default

---

## 🧱 Build the Docker Image

Build the agent image using the provided Dockerfile:

```bash
docker build -t case_study_matcher .
```

---

## 🐳 Run the Project with Docker Compose

Start the full stack (agent + Redis + Postgres):

```bash
docker-compose up --build
```

You should see logs confirming that Redis, Postgres, and the API service (`case_study_matcher`) are healthy.

**Alternative**: Run just the agent container without dependencies:

```bash
docker build -t case_study_matcher .
docker run -p 8123:8000 --env-file .env case_study_matcher
```

**Note**: The LangGraph API base image requires a `DATABASE_URI` environment variable. Docker Compose automatically sets this to PostgreSQL, but for standalone Docker you can use `DATABASE_URI=sqlite:///./langgraph.db`.

---

## 🌐 Accessing the Application

- **Agent Base URL**: `http://localhost:8123`
- **API Docs (FastAPI/Swagger)**: `http://localhost:8123/docs`
- **LangGraph Studio (connect to local agent)**: `https://smith.langchain.com/studio/?baseUrl=http://localhost:8123`

---

## 🔁 Exposed Services

| Service               | Host Port | Container Port | Description                 |
| --------------------- | --------- | -------------- | --------------------------- |
| Case Study Matcher    | 8123      | 8000           | Graph API via LangGraph     |
| PostgreSQL            | 5433      | 5432           | Persistent database         |
| Redis                 | 6379      | 6379           | Cache / state store         |

---

## 🗃️ Volumes

Docker volume created for persistent Postgres data:

```yaml
volumes:
  langgraph-data:
    driver: local
```

---

## ✅ Healthchecks

Docker Compose waits for `redis` and `postgres` to be healthy before starting the agent:

- Redis: `redis-cli ping`
- Postgres: `pg_isready -U postgres`


---

## 🚀 Interacting via SDK

Install the SDK locally and connect to the running agent:

```bash
pip install langgraph-sdk
```

Example (async):

```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:8123")

# Create a new thread
thread = await client.threads.create()
thread_id = thread["thread_id"]

assistant_id = "case_study_matcher"

# Input with project details
message_input = {
    "project_title": "Solar Power for Rural Communities",
    "problem_statement": "Lack of reliable electricity in rural African villages",
    "proposed_solution": "Implement solar microgrids with battery storage"
}

# Stream a run
async for event in client.runs.stream(
    thread_id,
    assistant_id,
    input=message_input,
    stream_mode="updates",
):
    print(event)
```

---

## 🔧 Local Development

For local development without Docker:

```bash
# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the agent locally
langgraph dev
```

---


## 📊 Input Schema

The agent expects the following structured input:

```python
{
    "project_title": str,        # Your project's title
    "problem_statement": str,    # Description of the problem you're solving
    "proposed_solution": str,    # Your proposed solution approach
    "query": str,               # Generated search query (auto-generated)
    "case_studies": list[str]   # Retrieved case studies (auto-populated)
}
```

---

## 🎯 Use Cases

Perfect for:
- **Consultants** looking for relevant case studies to support proposals
- **Researchers** seeking examples of similar projects
- **Project Managers** wanting to learn from past implementations
- **Students** working on case study analysis assignments
- **Startups** researching market validation examples

---

## Troubleshooting

- **Database URI Error**: If you see `KeyError: "Config 'DATABASE_URI' is missing"`, Docker Compose should set this automatically. For standalone Docker, use `DATABASE_URI=sqlite:///./langgraph.db`
- **Search API Errors**: Verify your `TAVILY_API_KEY` is valid and has sufficient credits
- **OpenAI Errors**: Check your `OPENAI_API_KEY` and ensure you have GPT-4 access
- **Port Conflicts**: If `8123` is occupied, change the host mapping in `docker-compose.yml` under the `ports:` section
- **LangSmith Issues**: Verify both `LANGSMITH_API_KEY` and `LANGCHAIN_TRACING_V2=true` are set in `.env`
- **Docker Issues**: Ensure Docker and Docker Compose are running and you have sufficient disk space

---

## 🤝 Contributing

This agent is built with:
- **LangGraph**: For workflow orchestration
- **LangChain**: For LLM integration and structured output
- **Tavily Search**: For web search capabilities
- **FastAPI**: For the REST API interface

Feel free to extend the agent with additional search sources, filtering capabilities, or enhanced query generation logic!
