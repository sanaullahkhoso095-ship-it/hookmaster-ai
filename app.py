
import os
import re
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="HookMaster AI | Viral Script Writer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL_NAME = "gemini-3.8-flash"


# ==========================================================
# 2. CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #0b1020 0%,
        #111827 55%,
        #101629 100%
    );
    color: #f8fafc;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #293449;
}

.hero {
    text-align: center;
    padding: 35px 15px 25px 15px;
    border: 1px solid #334155;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #172554,
        #1e1b4b,
        #312e81
    );
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: clamp(30px, 5vw, 46px);
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: #cbd5e1;
    font-size: 16px;
}

.feature-card {
    background: #172033;
    border: 1px solid #334155;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    min-height: 115px;
}

.feature-card h3 {
    color: #a5b4fc;
    font-size: 16px;
}

.feature-card p {
    color: #cbd5e1;
    font-size: 13px;
}

.section-heading {
    color: #a5b4fc;
    font-weight: 700;
    font-size: 22px;
    margin-top: 20px;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 13px 20px;
    min-height: 48px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
}

.stTextArea textarea {
    background: #172033;
    color: white;
    border: 1px solid #475569;
    border-radius: 10px;
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 30px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. API KEY MANAGEMENT
# ==========================================================

def get_api_key():

    # First check Streamlit secrets
    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")

        if secret_key:
            return str(secret_key).strip()

    except Exception:
        pass

    # Otherwise check environment variable
    return os.environ.get("GEMINI_API_KEY", "").strip()


# API key is loaded silently.
# No API configuration box is displayed in the sidebar.

api_key = get_api_key()


# ==========================================================
# 4. GEMINI AI SCRIPT GENERATOR
# ==========================================================

def generate_video_script(
    api_key,
    topic,
    platform,
    language,
    tone,
    duration
):

    client = genai.Client(api_key=api_key)

    duration_seconds = 30 if duration == "30 Seconds" else 60

    prompt = f"""
You are HookMaster AI, a professional viral video scriptwriter,
social media strategist, and audience retention expert.

Create a complete, engaging, production-ready short-form video script.

VIDEO SETTINGS:

Topic: {topic}
Platform: {platform}
Language: {language}
Tone: {tone}
Duration: {duration_seconds} seconds

========================================
1. THREE VIRAL HOOKS
========================================

Generate exactly 3 unique scroll-stopping hooks.

Requirements:
- Capture attention within the first 3 seconds.
- Create curiosity, surprise, emotion, or suspense.
- Make each hook natural and easy to speak.
- Make hooks relevant to the topic.
- Avoid generic opening sentences.

========================================
2. COMPLETE SCENE-BY-SCENE SCRIPT
========================================

Write a complete script matching the requested duration.

Requirements:
- Divide the video into logical scenes.
- Include timestamps for every scene.
- Include exact spoken dialogue or voiceover.
- Include visual directions in square brackets.
- Include camera movements and zoom effects.
- Include B-roll and transitions where appropriate.
- Include on-screen text.
- Maintain audience curiosity throughout.
- Build towards a satisfying ending.
- Avoid unnecessary introductions and filler.

The total scene timestamps must cover the complete video duration.

========================================
3. STRONG CALL TO ACTION
========================================

Write an engaging CTA encouraging viewers to interact.

Encourage comments, shares, saves, or follows naturally.

========================================
4. CATCHY VIDEO TITLE
========================================

Create one curiosity-driven title suitable for the selected platform.

========================================
5. VIDEO CAPTION
========================================

Write an engaging social media caption.
Include a relevant question or conversational element.

========================================
6. EXACTLY 10 HASHTAGS
========================================

Generate exactly 10 relevant hashtags.

Requirements:
- Mix broad and niche hashtags.
- Match the selected platform and topic.
- Avoid duplicate hashtags.
- Do not claim that popularity has been verified in real time.

========================================
LANGUAGE REQUIREMENTS
========================================

Use the selected language consistently:

English:
Natural, fluent English.

Roman Urdu:
Urdu written in English/Roman characters.

Urdu (Nastaliq):
Natural Urdu written in Urdu script.

Hindi:
Natural Hindi written in Devanagari script.

Production instructions such as [Zoom in] and
[Show text on screen] may remain in English.

========================================
OUTPUT FORMAT
========================================

# 🎬 HOOKMASTER AI - VIDEO SCRIPT

## 1. 🔥 THREE VIRAL HOOKS

### Hook 1
[Hook text]

### Hook 2
[Hook text]

### Hook 3
[Hook text]

## 2. 🎥 COMPLETE SCENE-BY-SCENE SCRIPT

### Scene 1 - [Timestamp]

**Visual Direction:** [Camera and visual instructions]

**Voiceover / Dialogue:** [Exact spoken words]

**On-Screen Text:** [Text displayed on screen]

**Transition:** [Transition instructions]

Repeat this format for every scene.

## 3. 🚀 FINAL CALL TO ACTION

[Strong CTA]

## 4. ✨ CATCHY VIDEO TITLE

[Title]

## 5. 📝 SOCIAL MEDIA CAPTION

[Caption]

## 6. #️⃣ 10 HASHTAGS

[Exactly 10 hashtags]

========================================
FINAL QUALITY CHECK
========================================

- Include every requested section.
- Keep the script practical for creators.
- Use natural, engaging language.
- Respect the requested video duration.
- Do not provide multiple full scripts.
- Do not explain your writing process.
- Return only the finished script in Markdown.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.85,
            top_p=0.95,
            max_output_tokens=8192
        )
    )

    if not response.text or not response.text.strip():
        raise ValueError(
            "Gemini returned an empty response. Please try again."
        )

    return response.text.strip()


# ==========================================================
# 5. SIDEBAR - VIDEO SETTINGS ONLY
# ==========================================================

with st.sidebar:

    st.markdown("## 🎬 HookMaster AI")

    st.caption("Your AI-powered viral content studio")

    st.divider()

    st.markdown("### ⚙️ Video Settings")

    platform = st.selectbox(
        "Choose Platform",
        [
            "TikTok",
            "Instagram Reels",
            "YouTube Shorts"
        ]
    )

    language = st.selectbox(
        "Select Language",
        [
            "English",
            "Roman Urdu",
            "Urdu (Nastaliq)",
            "Hindi"
        ]
    )

    tone = st.selectbox(
        "Choose Video Style",
        [
            "Energetic & Fast-Paced",
            "Storytelling & Emotional",
            "Educational & Informative",
            "Funny & Relatable"
        ]
    )

    duration = st.radio(
        "Video Duration",
        [
            "30 Seconds",
            "60 Seconds"
        ]
    )

    st.divider()

    st.markdown("### 💡 Pro Tip")

    st.info(
        "Use specific topics instead of broad ideas. "
        "For example: '5 mistakes beginners make in digital marketing' "
        "instead of just 'Digital Marketing'."
    )

    st.caption("Powered by Google Gemini 2.5 Flash")



# ==========================================================
# 6. MAIN HEADER
# ==========================================================

st.markdown("""
<div class="hero">
    <h1>🎬 HookMaster AI</h1>
    <p>Viral Reels & Shorts Script Writer</p>
    <p>Turn your ideas into attention-grabbing video scripts.</p>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# 7. FEATURE CARDS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🔥 Viral Hooks</h3>
        <p>3 attention-grabbing openings</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🎥 Smart Scripts</h3>
        <p>Scene-by-scene storytelling</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 Powerful CTA</h3>
        <p>Drive comments and shares</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>📈 SEO Hashtags</h3>
        <p>10 relevant hashtags</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# 8. TOPIC INPUT
# ==========================================================

st.markdown(
    '<p class="section-heading">💡 What is your video about?</p>',
    unsafe_allow_html=True
)

topic = st.text_area(
    "Enter your video topic",
    placeholder=(
        "Example: 5 AI tools that can save you 10 hours every week..."
    ),
    height=120,
    max_chars=2000,
    label_visibility="collapsed"
)

st.caption(
    f"{len(topic)} / 2000 characters | "
    f"Platform: {platform} | Duration: {duration}"
)


# ==========================================================
# 9. GENERATE BUTTON
# ==========================================================

generate_button = st.button(
    "🚀 Generate My Viral Script",
    type="primary",
    use_container_width=True
)


# ==========================================================
# 10. GENERATION AND ERROR HANDLING
# ==========================================================

if generate_button:

    # Clear previous output when starting a new generation
    st.session_state.pop("generated_script", None)
    st.session_state.pop("generated_topic", None)

    if not topic.strip():

        st.error(
            "⚠️ Please enter a video topic before generating."
        )

    elif not api_key:

        st.error(
            "🔑 Gemini API key is missing. "
            "Please configure GEMINI_API_KEY in your secrets.toml "
            "or environment variables."
        )

    else:

        try:

            with st.spinner(
                "🔥 HookMaster AI is crafting your viral script..."
            ):

                generated_script = generate_video_script(
                    api_key=api_key,
                    topic=topic.strip(),
                    platform=platform,
                    language=language,
                    tone=tone,
                    duration=duration
                )

            st.session_state["generated_script"] = generated_script
            st.session_state["generated_topic"] = topic.strip()

            st.success(
                "🎉 Your video script has been generated successfully!"
            )

        except APIError as error:

            status_code = getattr(error, "code", None)

            if status_code in (400,):

                st.error(
                    "Invalid request. Please check your input "
                    "and Gemini model availability."
                )

            elif status_code in (401, 403):

                st.error(
                    "Authentication failed. Your Gemini API key "
                    "may be invalid, restricted, or unauthorized."
                )

            elif status_code == 429:

                st.error(
                    "Gemini API quota or rate limit reached. "
                    "Please check your Google AI Studio usage "
                    "and try again later."
                )

            else:

                st.error(
                    f"Gemini API error ({status_code}): {error}"
                )

        except ValueError as error:

            st.error(str(error))

        except Exception as error:

            st.error(
                "An unexpected error occurred while generating "
                f"your script. Details: {error}"
            )


# ==========================================================
# 11. DISPLAY GENERATED SCRIPT
# ==========================================================

if st.session_state.get("generated_script"):

    st.divider()

    st.markdown(
        '<p class="section-heading">'
        '✨ Your Generated Video Script'
        '</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"**Topic:** {st.session_state.get('generated_topic', '')}"
    )

    st.markdown(
        st.session_state["generated_script"]
    )

    st.divider()

    script_text = st.session_state["generated_script"]

    safe_topic = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        st.session_state.get(
            "generated_topic",
            "video_script"
        )
    ).strip("_")[:50] or "video_script"

    st.download_button(
        label="📥 Download Script (.txt)",
        data=script_text.encode("utf-8"),
        file_name=f"HookMaster_{safe_topic}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.caption(
        "Your generated script is ready to copy, edit, "
        "or use for your next video."
    )




# ==========================================================
# 12. FOOTER
# ==========================================================

st.divider()

st.markdown(
    "HookMaster AI © 2026 | Powered by Google Gemini"
)

st.caption(
    "Create smarter. Capture attention. Tell better stories."
)


    Create smarter. Capture attention. Tell better stories.

</div>
""", unsafe_allow_html=True)
