Output demo.gif

Set Shell bash
Set FontSize 18
Set Width 1200
Set Height 700
Set Padding 25
Set Framerate 30
Set TypingSpeed 45ms
Set Theme "Dracula"

# Prepare the project perfectly
Hide
Type "source ../venv/bin/activate || source venv/bin/activate"
Enter
Type "export OPENROUTER_API_KEY=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"
Enter
Type "export PYDANTIC_AI_NO_BANNER=1"
Enter
Type "clear"
Enter
Show

Sleep 1s
Type "echo 'SCHEMA HEALER  |  SELF-HEALING ANALYTICS'"
Enter
Type "echo 'Schema discovery  /  SQL guardrails  /  bounded recovery'"
Enter
Type "echo"
Enter
Sleep 2s

# Run the engine as a clean module
Type "python3 -m src.engine"
Enter

# Give it 45 seconds to crash and heal
Sleep 45s