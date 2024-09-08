import streamlit as st
import requests
import json


st.title('Easy Checker')

source = st.text_input("Insert character.ai link", placeholder="https://character.ai/chat/...")

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
        st.text(f"""
                **Tagline**: {response["title"]}  
                **Greeting**: {len(response["greeting"])} characters  
                **Descrition**: {len(response["description"])} characters  
                **Definition**: {len(response["definition"])} characters  
        """)
        with st.expander("Copy everything", expanded=False, icon=None):
            copy = f"""
                # Name: {response["name"]}
                ### Link: https://character.ai/chat/{externalId}
                ### Creator: {response["user__username"]}\n
                ### Tagline:\n{response["title"]}\n
                ### Greeting:\n{response["greeting"]}\n
                ### Descrition:\n{response["description"]}\n
                ### Definition:\n{response["definition"]}\n
                """
            st.code(copy, language='markdown', wrap_lines=False)
    st.text_area("GREETING", value=response["greeting"], height=350)
    st.text_area("DESCRIPTION", value=response["description"], height=180)
    st.text_area("DEFINITON", value=response["definition"], height=500)
