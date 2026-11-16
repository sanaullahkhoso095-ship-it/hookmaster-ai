
import os
import re
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HookMaster AI | Viral Script Writer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #111827 55%, #101629 100%);
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
        background: linear-gradient(135deg, #172554, #1e1b4b, #312e81);
        margin-bottom: 25px;
    }

    .hero h1 {
        color: #ffffff;
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
        border: none;
        color: white;
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

    div[data-testid="stMarkdownContainer"] p {
        line-height: 1.7;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API KEY MANAGEMENT
# ============================================================

def get_configured_api_key():
    """Read API key from Streamlit secrets or environment."""

    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
        if secret_key:
            return str(secret_key).strip()
    except Exception:
        pass

    return os.environ.get("GEMINI_API_KEY", "").strip()


# ============================================================
# GEMINI SCRIPT GENERATOR
# ============================================================

def generate_video_script(
    api_key: str,
    topic: str,
    platform: str,
    language: str,
    tone: str,
    duration: str,
) -> str:
    """Generate a complete short-form video script using Gemini."""

    client = genai.Client(api_key=api_key)

    duration_seconds = 30 if duration == "30 Seconds" else 60

    prompt = f"""
You are HookMaster AI, an expert viral short-form video scriptwriter,
social media strategist, and audience-retention specialist.

Your task is to create a highly engaging, production-ready video script.

================ VIDEO SETTINGS ================

VIDEO TOPIC:
{topic}

PLATFORM:
{platform}

LANGUAGE:
{language}

TONE:
{tone}

VIDEO DURATION:
{duration_seconds} seconds

================ CONTENT REQUIREMENTS ================

1. VIRAL HOOKS

Generate exactly 3 different scroll-stopping hooks.

Each hook must:
- Grab attention within the first 3 seconds.
- Create curiosity, surprise, emotion, or a strong knowledge gap.
- Be natural and easy to speak.
- Be relevant to the topic.

2. COMPLETE VIDEO SCRIPT

Create a complete scene-by-scene script.

Requirements:
- Match the requested {duration_seconds}-second duration.
- Divide the script into logical scenes with timestamps.
- Include spoken dialogue / voiceover for every scene.
- Add visual directions in square brackets.
- Include camera movements, zooms, transitions, B-roll,
  facial expressions, and on-screen text where appropriate.
- Maintain audience curiosity throughout.
- Avoid unnecessary introductions and filler.
- Make the opening particularly powerful.
- Build toward a satisfying payoff.
- Keep dialogue natural and suitable for speaking aloud.

3. CALL TO ACTION

Create a powerful closing CTA that encourages viewers to:
- Comment.
- Share.
- Save.
- Follow the account.

Use a natural CTA rather than a generic sales pitch.
Do not force all four actions into one sentence.

4. VIDEO TITLE

Write one catchy, curiosity-driven title suitable for the platform.

5. VIDEO CAPTION

Write an engaging social media caption.
Include a relevant question or conversational element.

6. HASHTAGS

Generate exactly 10 relevant hashtags.

Hashtag requirements:
- Mix broad and niche topic-related hashtags.
- Make them relevant to the selected platform.
- Avoid inventing claims that hashtags are currently trending.
- Do not repeat hashtags.

================ LANGUAGE RULES ================

Use the selected language consistently throughout the hooks,
dialogue, CTA, title, and caption.

Language selection:
- English: Natural, fluent English.
- Roman Urdu: Urdu written using English/Roman characters.
- Urdu (Nastaliq): Natural Urdu in Urdu script.
- Hindi: Natural Hindi in Devanagari script.

Visual production instructions such as [Zoom in] and [Show text
on screen] may remain in English for clarity.

================ OUTPUT FORMAT ================

Use the following Markdown structure:

# 🎬 HOOKMASTER AI - VIDEO SCRIPT

## 1. 🔥 THREE VIRAL HOOKS

### Hook 1
[Hook text]

### Hook 2
[Hook text]

### Hook 3
[Hook text]

## 2. 🎥 COMPLETE SCENE-BY-SCENE SCRIPT

For every scene include:

### Scene [Number] - [Timestamp]
**Visual Direction:** [Camera and visual instructions]

**Voiceover / Dialogue:** [Exact spoken words]

**On-Screen Text:** [Text displayed on screen]

**Transition:** [Transition instructions]

Ensure the scene timestamps cover the complete requested duration.

## 3. 🚀 FINAL CALL TO ACTION

[Strong CTA]

## 4. ✨ CATCHY VIDEO TITLE

[Title]

## 5. 📝 SOCIAL MEDIA CAPTION

[Caption]

## 6. #️⃣ 10 HASHTAGS

[Exactly 10 hashtags]

================ QUALITY CONTROL ================

- Do not omit any requested section.
- Do not provide explanations about your writing process.
- Do not include multiple alternative full scripts.
- Do not exceed the requested duration unnecessarily.
- Make the script practical for an actual content creator.
- Return only the finished script in the requested format.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.85,
            top_p=0.95,
            max_output_tokens=8192,
        ),
    )

    result = response.text

    if not result or not result.strip():
        raise ValueError(
            "Gemini returned an empty response. Please try again."
        )

    return result.strip()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎬 HookMaster AI")

    st.caption("Your AI-powered viral content studio")

    st.divider()

    st.markdown("### 🔐 API Configuration")

    configured_key = get_configured_api_key()

    manual_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Enter your Gemini API key",
        help="Your key is used only for the current application session.",
    )

    api_key = manual_api_key.strip() if manual_api_key.strip() else configured_key

    if api_key:
        st.success("API key configured")
    else:
        st.warning("Please configure your Gemini API key.")

    st.divider()

    st.markdown("### ⚙️ Video Settings")

    platform = st.selectbox(
        "Choose Platform",
        [
            "TikTok",
            "Instagram Reels",
            "YouTube Shorts",
        ],
        index=0,
    )

    language = st.selectbox(
        "Select Language",
        [
            "English",
            "Roman Urdu",
            "Urdu (Nastaliq)",
            "Hindi",
        ],
        index=0,
    )

    tone = st.selectbox(
        "Choose Video Style",
        [
            "Energetic & Fast-Paced",
            "Storytelling & Emotional",
            "Educational & Informative",
            "Funny & Relatable",
        ],
        index=0,
    )

    duration = st.radio(
        "Video Duration",
        [
            "30 Seconds",
            "60 Seconds",
        ],
        index=0,
    )

    st.divider()

    st.markdown("### 💡 Pro Tip")

    st.info(
        "Use specific topics instead of broad ideas. "
        "For example: '5 mistakes beginners make in digital marketing' "
        "instead of just 'Digital Marketing'."
    )

    st.caption("Powered by Google Gemini 2.5 Flash")


# ============================================================
# MAIN APPLICATION HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🎬 HookMaster AI</h1>
        <p>Viral Reels & Shorts Script Writer</p>
        <p>Turn your ideas into attention-grabbing video scripts.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🔥 Viral Hooks</h3>
            <p>3 attention-grabbing openings</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🎥 Smart Scripts</h3>
            <p>Scene-by-scene storytelling</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <h3>🚀 Powerful CTA</h3>
            <p>Drive comments and shares</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="feature-card">
            <h3>📈 SEO Hashtags</h3>
            <p>10 relevant hashtags</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TOPIC INPUT
# ============================================================

st.markdown(
    '<p class="section-heading">💡 What is your video about?</p>',
    unsafe_allow_html=True,
)

topic = st.text_area(
    "Enter your video topic",
    placeholder=(
        "Example: 5 AI tools that can save you 10 hours every week..."
    ),
    height=120,
    max_chars=2000,
    label_visibility="collapsed",
)

st.caption(
    f"{len(topic)} / 2000 characters | "
    f"Platform: {platform} | Duration: {duration}"
)


# ============================================================
# GENERATE SCRIPT BUTTON
# ============================================================

generate_button = st.button(
    "🚀 Generate My Viral Script",
    type="primary",
    use_container_width=True,
)


# ============================================================
# GENERATION & ERROR HANDLING
# ============================================================

if generate_button:

    if not topic.strip():
        st.error("⚠️ Please enter a video topic before generating.")

    elif not api_key:
        st.error(
            "🔑 Gemini API key is missing. "
            "Enter your key in the sidebar or configure GEMINI_API_KEY."
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
                    duration=duration,
                )

            st.session_state["generated_script"] = generated_script
            st.session_state["generated_topic"] = topic.strip()

            st.success("🎉 Your video script has been generated!")

        except APIError as error:

            status_code = getattr(error, "code", None)
            error_message = str(error)

            if status_code == 400:
                st.error(
                    "Invalid request. Please check your input and "
                    "confirm that the selected model is available."
                )

            elif status_code in (401, 403):
                st.error(
                    "Authentication failed. Your Gemini API key may be "
                    "invalid, restricted, or unauthorized."
                )

            elif status_code == 429:
                st.error(
                    "Gemini API quota or rate limit reached. "
                    "Please check your Google AI Studio usage and "
                    "billing settings, then try again later."
                )

            else:
                st.error(
                    f"Gemini API error ({status_code}): {error_message}"
                )

        except ValueError as error:
            st.error(str(error))

        except Exception as error:
            st.error(
                "An unexpected error occurred while generating your script. "
                "Please try again. Details: " + str(error)
            )


# ============================================================
# DISPLAY GENERATED SCRIPT
# ============================================================

if st.session_state.get("generated_script"):

    st.divider()

    st.markdown(
        '<p class="section-heading">✨ Your Generated Video Script</p>',
        unsafe_allow_html=True,
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
        st.session_state.get("generated_topic", "video_script"),
    ).strip("_")[:50] or "video_script"

    st.download_button(
        label="📥 Download Script (.txt)",
        data=script_text.encode("utf-8"),
        file_name=f"HookMaster_{safe_topic}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.caption(
        "Your generated script is ready to copy, edit, or use "
        "for your next video."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        HookMaster AI © 2026 | Powered by Google Gemini<br>
        Create smarter. Capture attention. Tell better stories.
    </div>
    """,
    unsafe_allow_html=True,
)
