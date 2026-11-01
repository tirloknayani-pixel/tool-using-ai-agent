# Tool-Using Task Assistant
A working rule-based tool router with four tools: safe arithmetic calculator, date lookup, word counter, and uppercase text converter. Displays the selected tool, arguments, and result for transparency.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
Try `calculate (12+8)*3`, `date`, `word count hello world`, `uppercase hello`.

## Limits
This is a tool-calling **foundation/demo**, not an autonomous LLM agent. The calculator uses a restricted AST parser, not `eval`.
