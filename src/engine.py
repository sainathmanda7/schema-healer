from src.state import AgentState
from src.agents import router_agent, sql_agent
import src.tools  # Crucial: registers the tools with the sql_agent

def run_analytical_session(user_input: str):
    state = AgentState()
    
    print("\n--- Phase 1: Context Routing ---")
    routed_request = router_agent.run_sync(user_input).output
    print(f"Rewritten Request: {routed_request}")

    print("\n--- Phase 2: Agentic Execution ---")
    max_iterations = 3
    iteration = 0
    message_history = [] 

    while iteration < max_iterations:
        iteration += 1
        print(f"\n[Circuit Breaker] Attempt {iteration}/{max_iterations}")
        
        try:
            result = sql_agent.run_sync(
                routed_request, 
                deps=state, 
                message_history=message_history
            )
            print(f"\nFINAL ANSWER: {result.output}")
            return 
            
        except Exception as e:
            print(f"Agent Framework Error: {e}")
            break 

    print("\n[SYSTEM] Circuit breaker tripped. Maximum LLM iterations reached without resolving the query.")

if __name__ == "__main__":
    prompt = "Get total spending by user email ordered by account creation date"
    run_analytical_session(prompt)