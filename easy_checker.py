import streamlit as st # type: ignore
import requests
import json
import os

from tavern_cards import Card

st.title('Easy Checker')

tab_cai, tab_card = st.tabs(["🤖 C.ai", "🃏 Cards"])


def length_check(definition):
    if definition <= 3000:
        return f":sos: {definition}"
    return f":white_check_mark: {definition}"
def get_cai_data(link):
    externalId = link.split("/")[-1]
    trpc_json = (f'https://character.ai/api/trpc/character.infoCached?batch=1&input=%7B"0"%3A%7B"json"%3A%7B"externalId"%3A"{externalId}"%7D%7D%7D')
    response = requests.get(trpc_json).json()[0]['result']['data']['json']['character']
    return response

with tab_cai:
    cai_link = st.text_input("Insert character.ai link", placeholder="https://character.ai/chat/...")
    if cai_link:
        cai_bot = get_cai_data(cai_link)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(f"https://characterai.io/i/400/static/avatars/{cai_bot["avatar_file_name"]}")
        with col2:
            st.subheader(f"""
            [{cai_bot["name"]}](https://character.ai/chat/{cai_bot["external_id"]}) by [{cai_bot["user__username"]}](https://character.ai/profile/{cai_bot["user__username"]})
            """)
            st.markdown(f"""
                    **Tagline**: {cai_bot["title"]}  
                    **Greeting**: {len(cai_bot["greeting"])} characters  
                    **Descrition**: {len(cai_bot["description"])} characters  
                    **Definition**: {length_check(len(cai_bot["definition"]))} characters  
            """)
            with st.expander("Copy everything", expanded=False, icon=None):
                copy = f"""# Name: {cai_bot["name"]}\nLink: https://character.ai/chat/{cai_bot["external_id"]}\nCreator: {cai_bot["user__username"]}\nTagline: {cai_bot["title"]}\n---\n# Greeting:\n{cai_bot["greeting"]}\n\n# Description:\n{cai_bot["description"]}\n\n# Definition:\n{cai_bot["definition"]}\n"""
                st.markdown("""[:writing_hand: Create Google Doc](https://doc.new) | [:memo: Open Quillbot](https://quillbot.com/grammar-check)"""
                )
                st.code(copy, language='markdown', wrap_lines=False)
        st.text_area(f"GREETING, {len(cai_bot["greeting"])}", value=cai_bot["greeting"], height=350)
        st.text_area(f"DESCRIPTION, {len(cai_bot["description"])}", value=cai_bot["description"], height=180)
        st.text_area(f"DEFINITON, {len(cai_bot["definition"])}", value=cai_bot["definition"], height=500)
with tab_card:
    st.warning('This tool works correctly only with JSON files exported from Agnai or Silly tavern', icon="⚠️")
    card_json_upload = st.file_uploader("Upload card .json file", type='json')
    if card_json_upload:
        card_json = card_json_upload.getvalue().decode("utf-8")        
        card_json = json.loads(card_json)
        card = Card(card_json)

        f"""
        # {card.name} by {card.creator}
        
        ### **STATS**:
        * Card spec version: {card.spec}
        * Permanent characters: {f'**:red[! {card.len_permanent}]**' if 3000 > card.len_permanent else card.len_permanent}
        * Temporal characters: {card.len_temporal}  
        * Lorebook: {card.lorebook_name}, {card.len_lb_entries} total symbols in {card.num_lb_entries} entries 
        * Alt greetings: {"No" if card.temp_content['alternate_greetings'] is False else "Yes"}
        
        ### TAGS"""
        st.multiselect("Character's tags", card.tags, card.tags, label_visibility="collapsed")
        
        """### CREATOR COMMENT""" 
        card.creator_comment

        st.subheader("Prompt replacements", divider=True)
        replacements = f"""system prompt: {card.prompts['system_prompt']}\n
post-history: {card.prompts['post_history_instructions']}\n
in-depth prompt: {card.prompts['depth_prompt']}\n"""
        st.code(replacements,
                language='markdown',
                wrap_lines=True)

        st.subheader(f"Permanent content, {card.len_permanent} chars", divider=True)
        permanent = "\n".join([f'# {key}\n{value}\n' for key, value in card.permanent_content.items()])
        st.code(permanent,
                language='markdown',
                wrap_lines=True)
        
        st.subheader(f"Temporal content, {card.len_temporal} chars", divider=True)
        temporal = "\n".join([f'# {key}\n{value}\n' for key, value in card.temp_content.items()])
        st.code(temporal,
                language='markdown',
                wrap_lines=True)
        
        if card.lorebook_name != 'No lorebook':
            lorebook = "\n".join([f'''# {value['name']}\nTags: {", ".join(value['keys'])}\nContent: {value['content']}\n***''' 
                        for value in card.lorebook_entries])
            st.subheader(f"Lorebook: {card.lorebook_name}", divider=True)
            st.code(lorebook,
                    language='markdown',
                    wrap_lines=True)