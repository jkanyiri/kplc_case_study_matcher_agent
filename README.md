# 📚 Case Study Matcher Agent

An intelligent agent that helps find relevant case studies for your projects by analyzing project titles, problem statements, and proposed solutions. The agent uses LangGraph to orchestrate a workflow that generates optimized search queries and retrieves relevant case studies from the web.

## 🎯 What It Does

The Case Study Matcher Agent:

1. **Takes a Message**: Receives your project idea as a single message input
2. **Analyzes Project Context**: Processes your project description to understand the context
3. **Generates Smart Queries**: Uses AI to create optimized search queries for finding relevant case studies
4. **Searches the Web**: Leverages Tavily Search to find up to 20 relevant case studies
5. **Returns Results**: Provides you with a curated list of case studies that match your project needs

## 🏗️ Architecture

Built with LangGraph, the agent follows a simple but effective workflow:

- **Message Input**: Receives your project details as a message
- **Generate Query Node**: AI-powered query generation based on project context
- **Search Case Studies Node**: Web search using Tavily Search API
- **State Management**: Tracks project details, generated queries, and search results
- **Result Output**: Returns the complete analysis with relevant case studies

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
```

Notes:

- `OPENAI_API_KEY` is required for the agent to generate intelligent search queries
- `TAVILY_API_KEY` is required for web search functionality
- `LANGSMITH_API_KEY` is optional, only needed if you want tracing to LangSmith

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

---

## 🌐 Accessing the Application

- **Agent Base URL**: `http://localhost:8123`
- **API Docs (FastAPI/Swagger)**: `http://localhost:8123/docs`
- **LangGraph Studio (connect to local agent)**: `https://smith.langchain.com/studio/?baseUrl=http://localhost:8123`
- **LangGraph Studio (connect to production agent)**: `https://smith.langchain.com/studio/?baseUrl=https://match-maker-agent-production.up.railway.app`

## 🚀 Interacting with the Agent

### JavaScript/TypeScript SDK (Recommended for Frontend)

Install the JavaScript SDK:

```bash
npm install @langgraph-js/sdk
# or
yarn add @langgraph-js/sdk
```

**Basic Example:**

```javascript
import { getClient } from "@langgraph-js/sdk";

const client = getClient({ url: "http://localhost:8123" });

async function findCaseStudies(projectIdea) {
  try {
    // Create a new thread
    const thread = await client.threads.create();
    const threadId = thread.thread_id;

    const assistantId = "case_study_matcher";

    // Stream the run to get results
    const stream = client.runs.stream(
      threadId,
      assistantId,
      {
        input: {
          project_idea: projectIdea,
        },
      },
      { stream_mode: "updates" }
    );

    for await (const event of stream) {
      console.log("Event:", event);

      // Check if we have results
      if (event.type === "end" && event.data?.outputs?.case_studies) {
        return event.data.outputs.case_studies;
      }
    }
  } catch (error) {
    console.error("Error finding case studies:", error);
    throw error;
  }
}

// Usage
findCaseStudies("Build a real-time chat application with WebSocket")
  .then((caseStudies) => {
    console.log("Found case studies:", caseStudies);
  })
  .catch((error) => {
    console.error("Failed to find case studies:", error);
  });
```

**React Hook Example:**

```javascript
import { useState, useEffect } from "react";
import { getClient } from "@langgraph-js/sdk";

const client = getClient({ url: "http://localhost:8123" });

export function useCaseStudyMatcher() {
  const [loading, setLoading] = useState(false);
  const [caseStudies, setCaseStudies] = useState([]);
  const [error, setError] = useState(null);

  const findCaseStudies = async (projectIdea) => {
    setLoading(true);
    setError(null);

    try {
      const thread = await client.threads.create();
      const threadId = thread.thread_id;
      const assistantId = "case_study_matcher";

      const stream = client.runs.stream(
        threadId,
        assistantId,
        {
          input: {
            project_idea: projectIdea,
          },
        },
        { stream_mode: "updates" }
      );

      for await (const event of stream) {
        if (event.type === "end" && event.data?.outputs?.case_studies) {
          setCaseStudies(event.data.outputs.case_studies);
          break;
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { findCaseStudies, caseStudies, loading, error };
}
```

### Python SDK

Install the Python SDK locally and connect to the running agent:

```bash
pip install langgraph-sdk
```

**Basic Example:**

```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:8123")

# Create a new thread
thread = await client.threads.create()
thread_id = thread["thread_id"]

assistant_id = "case_study_matcher"

# Stream the run to get results
async for event in client.runs.stream(
    thread_id,
    assistant_id,
    input={
    "project_idea": "project idea details"
},
    stream_mode="updates",
):
    print(event)
```

---

## 📊 Response Structure

Both SDKs return results with the following structure:

```json
{
  "case_studies": [
    {
      "title": "Case Study Title",
      "url": "https://example.com/case-study",
      "content": "Brief description or content snippet",
      "score": 0.95,
      "raw_content": "Raw content if available"
    }
  ]
}
```

### Response Fields Explained

- **`case_studies`**: Array of relevant case studies found
- **`title`**: Title of the case study
- **`url`**: Direct link to the case study
- **`content`**: Brief description or content snippet
- **`score`**: Relevance score from search engine (0-1, higher is better)
- **`raw_content`**: Raw content if available (may be null)

---

## 🔧 Frontend Integration Tips

1. **Error Handling**: Always wrap API calls in try-catch blocks
2. **Loading States**: Use the streaming nature to show real-time progress
3. **Caching**: Consider caching results for similar project ideas
4. **Rate Limiting**: Implement appropriate delays between requests
5. **User Experience**: Show partial results as they come in via streaming

## 📚 Additional Resources

- [LangGraph JavaScript SDK](https://www.npmjs.com/package/@langgraph-js/sdk)
- [LangGraph Python SDK](https://python.langchain.com/docs/langgraph)
- [LangGraph Studio](https://smith.langchain.com/)
- [API Documentation](http://localhost:8123/docs) (when running locally)
