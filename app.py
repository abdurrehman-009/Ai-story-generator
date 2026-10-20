
import os
import json
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="ToonGenius AI Story Generator",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101027, #21133b);
    color: white;
}
h1, h2, h3 { color: #d9c4ff; }
.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #db2777);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 ToonGenius AI")
st.subheader("Turn your imagination into cartoon stories!")

st.write(
    "Create original cartoon stories, characters, dialogue, "
    "and scene prompts using artificial intelligence."
)

with st.sidebar:
    st.header("Story Settings")

    genre = st.selectbox(
        "Choose a genre",
        ["Adventure", "Comedy", "Fantasy", "Educational", "Friendship"]
    )

    audience = st.selectbox(
        "Audience",
        ["Children", "General audience"]
    )

    duration = st.selectbox(
        "Story duration",
        ["15 seconds", "30 seconds", "60 seconds"]
    )

    style = st.selectbox(
        "Cartoon style",
        ["3D Cartoon", "2D Cartoon", "Anime-inspired", "Storybook"]
    )

    language = st.selectbox(
        "Story language",
        ["English", "Urdu"]
    )

st.markdown("### ✍️ Describe your cartoon idea")

idea = st.text_area(
    "What should happen in your story?",
    placeholder=(
        "Example: A little dragon gets lost in a magical forest "
        "and a kind boy helps it find its family."
    ),
    height=130,
    max_chars=2000
)

def get_groq_client():
    api_key = None

    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

    api_key = api_key or os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)

if st.button("✨ Generate My Cartoon Story", use_container_width=True):
    if not idea.strip():
        st.warning("Please enter a cartoon story idea first.")
    else:
        client = get_groq_client()

        if client is None:
            st.error(
                "Groq API key is missing. Add GROQ_API_KEY "
                "in Streamlit Secrets or your local environment."
            )
        else:
            prompt = f"""
You are a creative cartoon storyteller and screenplay writer.

Create an original cartoon story using these settings:

Story idea: {idea}
Genre: {genre}
Audience: {audience}
Duration: {duration}
Visual style: {style}
Language: {language}

Return a well-organized story with these sections:

1. STORY TITLE
2. SHORT SUMMARY
3. CHARACTERS
   - Name
   - Appearance
   - Personality
   - Clothing and colors
4. COMPLETE STORY
   - Beginning
   - Main problem
   - Solution and ending
5. SCENE-BY-SCENE STORYBOARD
   For each scene include:
   - Scene number and approximate duration
   - Location and background
   - Character actions and expressions
   - Camera direction
   - Dialogue or narration
   - Detailed cartoon image-generation prompt
   - Detailed image-to-video animation prompt

Keep the story suitable for the selected audience.
Make the scenes visually interesting and consistent.
Make the length appropriate for the requested duration.
Do not claim that images or videos have already been generated.
"""

            try:
                with st.spinner("Creating your cartoon story..."):
                    response = client.chat.completions.create(
                        model=os.getenv(
                            "GROQ_MODEL",
                            "llama-3.3-70b-versatile"
                        ),
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an expert cartoon screenwriter. "
                                    "Write original, coherent stories with "
                                    "clear characters and visual scenes."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                        max_tokens=3500
                    )

                    story = response.choices[0].message.content

                if story:
                    st.session_state["generated_story"] = story
                    st.session_state["story_idea"] = idea
                else:
                    st.error("The AI returned an empty story.")

            except Exception as error:
                st.error(
                    "Story generation failed. Check your API key, "
                    "model availability, internet connection, and "
                    "Groq usage limits."
                )
                st.caption(str(error)[:500])

if st.session_state.get("generated_story"):
    st.divider()
    st.markdown("## 📖 Your Generated Cartoon Story")

    story = st.session_state["generated_story"]
    st.markdown(story)

    st.download_button(
        "⬇️ Download Story as Text",
        data=story,
        file_name="toongenius_cartoon_story.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.info(
        "Your story includes character descriptions and prompts. "
        "To generate actual cartoon images or animated videos, "
        "connect a compatible image or video generation service."
    )

st.divider()
st.caption("ToonGenius AI | AI-powered cartoon storytelling studio")
