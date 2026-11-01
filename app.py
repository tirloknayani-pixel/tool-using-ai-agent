import ast
import datetime
import operator
import re
import streamlit as st

st.set_page_config(page_title="Tool-Using Assistant", layout="centered")
st.title("Tool-Using Task Assistant")
st.caption("Deterministic tool routing demo with a visible execution trace. No LLM or external APIs required.")
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow}
def calculate(expression):
    if len(expression)>120: raise ValueError("Expression too long")
    def walk(node,depth=0):
        if depth>12: raise ValueError("Expression too complex")
        if isinstance(node,ast.Expression):return walk(node.body,depth+1)
        if isinstance(node,ast.Constant) and type(node.value) in (int,float) and abs(node.value)<1e9:return node.value
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
            val=walk(node.operand,depth+1);return val if isinstance(node.op,ast.UAdd) else -val
        if isinstance(node,ast.BinOp) and type(node.op) in OPS:
            a,b=walk(node.left,depth+1),walk(node.right,depth+1)
            if isinstance(node.op,ast.Pow) and abs(b)>10:raise ValueError("Exponent too large")
            ans=OPS[type(node.op)](a,b)
            if abs(ans)>1e12:raise ValueError("Result too large")
            return ans
        raise ValueError("Only arithmetic operators are allowed")
    return walk(ast.parse(expression,mode="eval"))
def route(message):
    msg=message.strip()
    if msg.lower().startswith("calculate "):
        expr=msg[10:].strip();return "calculator",{"expression":expr},str(calculate(expr))
    if msg.lower() in ("date","today","current date"):
        return "date",{},datetime.date.today().isoformat()
    if msg.lower().startswith("word count "):
        txt=msg[11:];return "word_count",{"text":txt},str(len(txt.split()))
    if msg.lower().startswith("uppercase "):
        txt=msg[10:];return "uppercase",{"text":txt},txt.upper()
    return "router",{"input":msg},"Try: calculate (12+8)*3, date, word count your text, or uppercase your text."
query=st.text_input("Enter a task",placeholder="calculate (12+8)*3")
if st.button("Run task"):
    try:
        name,args,result=route(query)
        st.success(result)
        with st.expander("Tool execution trace",expanded=True):
            st.json({"selected_tool":name,"arguments":args,"result":result})
    except (ValueError,ZeroDivisionError,SyntaxError,OverflowError) as exc:
        st.error(f"Could not complete task: {exc}")
st.caption("Rule-based assistant; does not autonomously plan, call third-party tools, or use a language model.")
