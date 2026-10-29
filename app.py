import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver

# Page Config
st.set_page_config(page_title="Enterprise AI Agent", page_icon="🤖", layout="centered")

st.title("🤖 Enterprise Support & Logistics Agent")
st.markdown("Powered by **LangGraph Memory**, **Groq (Qwen)**, and Custom Tools with Error Handling.")

# Define Tools with Robust Error Validation
@tool
def calculate_shipping_cost(weight_kg: float, distance_km: float) -> str:
    """Calculate the shipping cost based on package weight in kg and distance in km."""
    try:
        weight = float(weight_kg)
        distance = float(distance_km)
        
        if weight <= 0 or distance <= 0:
            return "Error: Weight and distance must be positive numerical values."
            
        cost = 5.0 + (weight * 2.5) + (distance * 0.1)
        return f"Shipping Cost: ${round(cost, 2)}"
    except (ValueError, TypeError) as e:
        return f"Tool Execution Error: Invalid input types provided. Weight and distance must be numbers. Details: {str(e)}"

@tool
def check_inventory_database(item_sku: str) -> str:
    """Check stock availability and warehouse location for a given product SKU."""
    try:
        if not item_sku or not isinstance(item_sku, str):
            return "Error: Invalid SKU format. Please provide a valid string SKU."
            
        clean_sku = item_sku.strip().upper()
        
        inventory = {
            "SKU-882": "In Stock - 45 units available in Warehouse A",
            "SKU-991": "Low Stock - Only 3 units left in Warehouse B",
            "SKU-104": "Out of Stock - Restock expected next Monday"
        }
        
        return inventory.get(clean_sku, f"SKU '{clean_sku}' not found in enterprise inventory system.")
    except Exception as e:
        return f"Database Lookup Error: Failed to retrieve inventory status. Details: {str(e)}"

tools = [calculate_shipping_cost, check_inventory_database]
tools_by_name = {tool.name: tool for tool in tools}

# Load API Key securely
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("⚠️ `GROQ_API_KEY` not found in Streamlit secrets! Please check `.streamlit/secrets.toml`.")
    st.stop()

# Initialize Model
model = ChatGroq(model="qwen/qwen3.8-27b", api_key=groq_api_key, temperature=0)
model_with_tools = model.bind_tools(tools)

# Build LangGraph workflow
def call_model(state: MessagesState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def call_tools(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    outputs = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_call_id = tool_call["id"]
        
        # Safe Tool Execution with Catch-All Error Recovery Loop
        if tool_name in tools_by_name:
            tool_fn = tools_by_name[tool_name]
            try:
                tool_output = tool_fn.invoke(tool_call["args"])
            except Exception as e:
                tool_output = f"Execution Error in '{tool_name}': {str(e)}. Please correct your arguments and try again."
        else:
            tool_output = f"Unknown Tool Error: Tool '{tool_name}' does not exist."
            
        outputs.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call_id))
        
    return {"messages": outputs}

workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", call_tools)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", lambda s: "tools" if s["messages"][-1].tool_calls else END, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

# Memory Checkpointer
memory = MemorySaver()
app_graph = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "enterprise-user-session"}}

# Streamlit Chat Interface State
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Sidebar options to clear chat
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🗑️ Clear Conversation"):
        st.session_state["messages"] = []
        st.rerun()

# Display chat history
for msg in st.session_state["messages"]:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# User input box
if user_input := st.chat_input("Ask me about shipping costs or inventory SKUs..."):
    user_msg = HumanMessage(content=user_input)
    st.session_state["messages"].append(user_msg)
    
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking and executing tools safely..."):
            result = app_graph.invoke({"messages": [user_msg]}, config=config)
            final_response = result["messages"][-1].content
            st.markdown(final_response)
            st.session_state["messages"] = result["messages"]