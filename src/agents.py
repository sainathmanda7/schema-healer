import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from openai import AsyncOpenAI
from src.state import AgentState

# Force dotenv to look in the root folder, not inside src/
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

openrouter_client = AsyncOpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=os.getenv("OPENROUTER_API_KEY")
)

model = OpenAIChatModel(
    'openai/gpt-4o-mini', 
    provider=OpenAIProvider(openai_client=openrouter_client)
)

# ... (keep the rest of your agent definitions exactly as they are)

router_agent = Agent(
    model,
    system_prompt=(
        "You are a standalone query rewriter. Read the user's prompt and any conversational history. "
        "Output a single, self-contained data request. Do NOT write SQL. "
        "Example: 'Compare top users.' -> 'Find the top users by spending amount, excluding internal accounts.'"
    )
)

sql_agent = Agent(
    model,
    deps_type=AgentState,
    system_prompt=(
        "You are a strict PostgreSQL/SQLite code generator. "
        "1. Call `search_schema` to find relevant tables. "
        "2. Call `safe_execute_sql` to run your query. "
        "3. If execution fails, analyze the error and try a different approach. "
        "4. Output only the final business answer."
    )
)