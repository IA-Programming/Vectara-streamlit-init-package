import streamlit as st
import os

from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader


st.set_page_config('Update VectaraDB', '📃')
st.title('Update VectaraDB 📃')

def clear_temp(folder_path='temp'):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
try:
    if 'vector_store' in st.session_state:

        media = st.selectbox('Choose media type:', ['Websites', 'Documents', 'YT Videos'])

        if media == 'Websites':
            web_url = st.text_input('Link to webpage:')
            if web_url:
                loader = AsyncHtmlLoader(web_url)
                raw_web_content = loader.load()
                html2text = Html2TextTransformer()
                clean_web_content = html2text.transform_documents(raw_web_content)
                st.session_state.vector_store.add_documents(clean_web_content)
                st.info('Web page scraped!')

        elif media == 'Documents':
            files = st.file_uploader('Upload documents:', 
                            ['md', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt'],
                            accept_multiple_files=True)
            if files:
                paths = []
                for file in files:
                    file_path = os.path.join('temp', file.name)
                    with open(file_path, 'wb') as f:
                        f.write(file.read())
                    paths.append(file_path)
                
                st.session_state.vector_store.add_files(paths)
                st.info('Documents shipped to database.')
                clear_temp()

        else:
            yt_url = st.text_input('Youtube Video URL:')
            if yt_url:
                loader = GenericLoader(YoutubeAudioLoader([yt_url], 'temp'), OpenAIWhisperParser())
                transcript = loader.load()
                st.session_state.vector_store.add_documents(transcript)
                st.info('YT audio transcripted!')
                clear_temp()

    else:
        st.warning('VectaraDB not connected!')

except AttributeError:
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None