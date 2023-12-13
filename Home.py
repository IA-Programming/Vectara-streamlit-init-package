import streamlit as st
from langchain.vectorstores import Vectara
from st_components.vectara_search import perform_vectara_search, display_vectara_results
import json

if "chat_history" not in  st.session_state:
    st.session_state['chat_history'] = []

st.set_page_config('Home', '📖')
st.title('VectaServe HomePage 📖')
msg = st.empty()
if 'vector_store' not in st.session_state:
    msg.info('There is no implemented method for credential authentication from Vectara, so ensure that you enter the correct details for this app to work.')
else:
    msg.success('Credentials submitted to Vectara! Try ingest or query endpoints to confirm the connection.')

st.markdown('<style>.css-w770g5{\
            width: 100%;}\
            .css-b3z5c9{    \
            width: 100%;}\
            .stButton>button{\
            width: 100%;}\
            </style>', unsafe_allow_html=True)

if 'vector_store' not in st.session_state:
    with st.sidebar:
        st.session_state['customer_id'] = st.text_input('Customer ID')
        st.session_state['corpus_id'] = st.text_input('Corpus ID')
        st.session_state['api_key'] = st.text_input('API Key', type='password')

        if st.session_state['customer_id'] and st.session_state['corpus_id'] and st.session_state['api_key'] and st.button('login in'):
            st.session_state['vector_store'] = Vectara(st.session_state['customer_id'], st.session_state['corpus_id'], st.session_state['api_key'])
            st.rerun()
else:
    search_term = st.text_input("How may I help you ?", value="",placeholder='Ask your query here')

    chat_history = st.session_state.get("chat_history", [])

    if st.button("Search"):
        if search_term:
            with st.spinner():
                search_results = perform_vectara_search(search_term)
            if search_results is None:
                st.stop()

            summary = search_results["responseSet"][0]["summary"][0]["text"]
            st.write(summary)
            display_vectara_results(search_results)
            chat_history.append(f"**You:** {search_term}")
            chat_history.append(f"**Bot:** {summary}")
            chat_history.append("---------------------------------------------")
                    
            
    with st.expander("**Chat History**"):
        chat_history_markdown = "\n\n".join(chat_history)
        st.sidebar.markdown(chat_history_markdown)

        st.session_state.chat_history = chat_history