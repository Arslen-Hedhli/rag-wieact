import streamlit as st
from src.chunks import chunk_text
from src.embedder import cos_sim
from src.scraper import scrape_first_conversations
from src.llm_client import generate_answer  

st.set_page_config(page_title="Farmer Assistant Chatbot", page_icon="🌱", layout="wide")

st.title("🌱 Farmer Assistant Chatbot")
st.write("Ask me questions about your crops, seeds, and farming practices!")

# Input box for the farmer’s query
query = st.text_input("❓ Ask your question:", placeholder="e.g., Why are tomatoes yellow?")

if st.button("Get Answer") and query:
    with st.spinner("Thinking... 🌾"):
        # Step 1: Scrape data dynamically
        res = scrape_first_conversations(query)

        # Step 2: Chunk each article separately and combine
        chunks = []
        for article in res:
            chunks.extend(chunk_text(article, chunk_size=500, overlap=50))

        # Step 3: Embed and compute similarity for each chunk
        emb_res = [cos_sim(query, chunk) for chunk in chunks]

        # Step 4: Flatten embedding results and pair with chunk
        paired_chunks = []
        for idx, emb in enumerate(emb_res):
            # If cos_sim returns a list/tuple like (score, chunk_text)
            if isinstance(emb, (list, tuple)):
                paired_chunks.append((emb[0], chunks[idx]))
            else:  # If cos_sim returns just a score
                paired_chunks.append((emb, chunks[idx]))

        # Step 5: Take top 5 chunks by similarity score
        top_chunks = [chunk for score, chunk in sorted(paired_chunks, key=lambda x: x[0], reverse=True)[:5]]

        # Step 6: Generate answer with top context
        answer = generate_answer(query, top_chunks)

    # Display the answer
    st.success("✅ Answer:")
    st.write(answer)

    # Optional: Show retrieved context for transparency
    with st.expander("🔍 See retrieved context"):
        st.write(res)
