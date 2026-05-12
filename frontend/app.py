import os
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://api:8080")

st.title("Node Registry")

health = requests.get(f"{API_URL}/health").json()
st.write(f"API status: {health['status']} | DB: {health['db']} | Active nodes: {health['nodes_count']}")

st.subheader("Nodes")
nodes = requests.get(f"{API_URL}/api/nodes").json()
if nodes:
    st.table(nodes)
else:
    st.info("No nodes registered.")

st.subheader("Register Node")
name = st.text_input("Name")
host = st.text_input("Host")
port = st.number_input("Port", min_value=1, max_value=65535, value=8080)
if st.button("Register"):
    r = requests.post(f"{API_URL}/api/nodes", json={"name": name, "host": host, "port": port})
    if r.status_code == 201:
        st.success("Node registered.")
        st.rerun()
    else:
        st.error(r.text)

st.subheader("Delete Node")
del_name = st.text_input("Node name to delete")
if st.button("Delete"):
    r = requests.delete(f"{API_URL}/api/nodes/{del_name}")
    if r.status_code == 204:
        st.success("Node deleted.")
        st.rerun()
    else:
        st.error(r.text)