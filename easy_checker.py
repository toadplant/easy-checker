import streamlit as st # type: ignore
import requests
import json


st.title('Easy Checker')

source = st.text_input("Insert character.ai link", placeholder="https://character.ai/chat/...")

def length_check(definition):
    if definition <= 3000:
        return f":sos: {definition}"
    return f":white_check_mark: {definition}"

if source:
    externalId = source.split("/")[-1]
    trpc_json = (f'https://character.ai/api/trpc/character.infoCached?batch=1&input=%7B"0"%3A%7B"json"%3A%7B"externalId"%3A"{externalId}"%7D%7D%7D')
    response = requests.get(trpc_json).json()[0]['result']['data']['json']['character']

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(f"https://characterai.io/i/400/static/avatars/{response["avatar_file_name"]}")
    with col2:
        st.subheader(f"""
        [{response["name"]}](https://character.ai/chat/{externalId}) by [{response["user__username"]}](https://character.ai/profile/{response["user__username"]})
        """)
        st.markdown(f"""
                **Tagline**: {response["title"]}  
                **Greeting**: {len(response["greeting"])} characters  
                **Descrition**: {len(response["description"])} characters  
                **Definition**: {length_check(len(response["definition"]))} characters  
        """)
        with st.expander("Copy everything", expanded=False, icon=None):
            copy = f"""# Name: {response["name"]}\nLink: https://character.ai/chat/{externalId}\nCreator: {response["user__username"]}\nTagline: {response["title"]}\n---\n# Greeting:\n{response["greeting"]}\n\n# Description:\n{response["description"]}\n\n# Definition:\n{response["definition"]}\n"""
            st.markdown("""[:writing_hand: Create Google Doc](https://doc.new) | [:memo: Open Quillbot](https://quillbot.com/grammar-check)"""
            )
            st.code(copy, language='markdown', wrap_lines=False)
    st.text_area(f"GREETING, {len(response["greeting"])}", value=response["greeting"], height=350)
    st.text_area(f"DESCRIPTION, {len(response["description"])}", value=response["description"], height=180)
    st.text_area(f"DEFINITON, {len(response["definition"])}", value=response["definition"], height=500)
