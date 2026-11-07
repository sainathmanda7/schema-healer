import sqlite3
import sqlglot
from sqlglot.errors import ParseError
from pydantic_ai import RunContext
from src.state import AgentState
from src.agents import sql_agent

@sql_agent.tool
def search_schema(ctx: RunContext[AgentState], keywords: str) -> str:
    """Mock RAG: Returns only table schemas matching the keywords."""
    results = {k: v for k, v in ctx.deps.schema_registry.items() if any(word in v.lower() for word in keywords.split())}
    return str(results) if results else "No matching tables found. Broaden search."

@sql_agent.tool
def safe_execute_sql(ctx: RunContext[AgentState], query: str) -> str:
    """Safely executes SQL with AST Hashing and EXPLAIN cost checks."""
    print(f"\n[Engine] Intercepting Query: {query}")
    
    try:
        ast_hash = hash(sqlglot.parse_one(query).sql())
        if ast_hash in ctx.deps.attempted_hashes:
            return "SYSTEM REJECTION: You already tried this exact logical query. Change your JOINs or filtering strategy."
        ctx.deps.attempted_hashes.add(ast_hash)
    except ParseError:
        return "SYSTEM REJECTION: Invalid SQL syntax."

    conn = sqlite3.connect(ctx.deps.db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(f"EXPLAIN QUERY PLAN {query}")
        plan = str(cursor.fetchall())
        if "SCAN TABLE enterprise_users" in plan: 
            conn.close()
            return "SYSTEM REJECTION: Query requires a full table scan on enterprise_users. Add a LIMIT or indexed WHERE clause."
    except Exception:
        pass

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        print(f"[Engine] Success: {results}")
        return str(results)
    except Exception as e:
        conn.close()
        error_msg = f"DATABASE ERROR: {str(e)}"
        print(f"[Engine] {error_msg}")
        return error_msg