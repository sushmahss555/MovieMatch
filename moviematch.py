import streamlit as st
import requests
import urllib.parse
from google import genai
from pydantic import BaseModel

# 1. Page Configuration for an Elite Theater Feel
st.set_page_config(
    page_title="MovieMatch | Premium AI Cinema Curator", 
    page_icon="🍿", 
    layout="wide"
)

# 2. SECURE API CREDENTIALS (Saves keys in Streamlit's cloud vault)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

client = genai.Client(api_key=GEMINI_API_KEY)

# 3. Premium Studio Styling Engine (Fixes Emoji Bleaching & Adds Depth)
st.markdown("""
<style>
    /* Import High-End Sans Serif Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
    }

    /* Living Fluid Ambient Background Gradient */
    .stApp {
        background: linear-gradient(-45deg, #050510, #0B0B26, #120A21, #020205);
        background-size: 400% 400%;
        animation: gradientWave 15s ease infinite;
        background-attachment: fixed;
    }
    
    @keyframes gradientWave {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Flexbox Header Structure to safeguard natural emoji rendering */
    .title-container {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 0px;
    }
    
    .title-emoji {
        font-size: 3.5rem;
    }

    .main-title {
        font-weight: 800;
        color: #FFFFFF;
        font-size: 3.5rem;
        letter-spacing: -1.5px;
        margin: 0;
    }
    
    .sub-title {
        color: #00F0FF;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 3px;
        margin-bottom: 40px;
        text-transform: uppercase;
        opacity: 0.9;
    }

    /* Premium Frosted Acrylic Welcome Panel */
    .welcome-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 30px;
        border-radius: 24px;
        margin-bottom: 40px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
    }

    /* Luxury Glassmorphic Display Cards */
    div[data-testid="stVerticalBlockBorderWithBorders"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-radius: 32px !important;
        padding: 28px !important;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Responsive Hover Lift with Cyberpunk Accents */
    div[data-testid="stVerticalBlockBorderWithBorders"]:hover {
        transform: translateY(-12px) scale(1.02) !important;
        border-color: rgba(255, 46, 147, 0.4) !important;
        box-shadow: 0 30px 60px rgba(255, 46, 147, 0.15) !important;
    }

    /* Style for Form Borders - Making it transparent so it doesn't break our premium aesthetic */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }

    /* Explicit styling for user input text indicators */
    label p {
        color: #E2E8F0 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. Initialize Multi-Page Memory Blocks
if "page" not in st.session_state:
    st.session_state.page = "input_page"
if "saved_mood" not in st.session_state:
    st.session_state.saved_mood = ""

# 5. Helper Function: Asynchronous Poster Fetching from TMDb
def get_movie_poster(title, year):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}&year={year}"
        response = requests.get(url).json()
        if response.get('results'):
            poster_path = response['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmorg/t/p/w500{poster_path}"
    except Exception:
        pass
    return "https://via.placeholder.com/500x750.png?text=Poster+Not+Found"

# 6. Structured Object Formatting Schemas
class MovieRecommendation(BaseModel):
    title: str
    year: int
    rating: float
    why_it_fits: str

class MovieList(BaseModel):
    movies: list[MovieRecommendation]


# ==========================================
# WINDOW VIEW 1: THE ENTER GATEWAY
# ==========================================
if st.session_state.page == "input_page":
    st.write("")
    st.write("")
    
    # Beautifully aligned header assets
    st.markdown('<div class="title-container"><span class="title-emoji">🍿</span><h1 class="main-title">MovieMatch</h1></div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">AI Cinema Engine</p>', unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="welcome-card">
            <h3 style="margin-top:0; color: #FFF; font-weight:600; font-size:1.4rem; letter-spacing: -0.5px;">✨ Welcome to the Lounge</h3>
            <p style="color: #94A3B8; font-size: 1rem; line-height: 1.7; margin-bottom: 0px;">
                Skip the platform choice exhaustion. Describe your current mental state or a niche thematic prompt, and our layout engine handles the rest.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # UPGRADE: Input wrapped inside a form to capture keyboard "Enter/Go" actions seamlessly
        with st.form("mood_entry_form", clear_on_submit=False):
            user_mood = st.text_input(
                "What kind of movie experience are you looking for?", 
                placeholder="e.g., Exhausted but wired. Need an atmospheric cyberpunk thriller..."
            )

            st.write("")
            st.write("")
            
            submit_button = st.form_submit_button("🎬 Begin Private Screening", use_container_width=True)
            
            if submit_button:
                if user_mood:
                    st.session_state.saved_mood = user_mood
                    st.session_state.page = "results_page"
                    st.rerun()
                else:
                    st.warning("Please tell the curator how you are feeling to engage the engine.")


# ==========================================
# WINDOW VIEW 2: THE THEATRICAL DISPLAY
# ==========================================
elif st.session_state.page == "results_page":
    st.write("")
    st.write("")
    
    st.markdown('<div class="title-container"><span class="title-emoji">🍿</span><h1 class="main-title">Your Screenings</h1></div>', unsafe_allow_html=True)
    st.markdown(f"<p style='color:#00F0FF; font-size:1rem; font-weight:600; text-transform:uppercase; margin-bottom:40px; letter-spacing:1px;'>🎯 CURATED VIBE: \"{st.session_state.saved_mood}\"</p>", unsafe_allow_html=True)

    with st.spinner("⚡ Calibrating screening array... parsing digital artwork files..."):
        prompt = f'Recommend exactly 3 movies for someone feeling: "{st.session_state.saved_mood}". Provide a comprehensive, high-quality analytical evaluation.'
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=dict(
                response_mime_type="application/json",
                response_schema=MovieList,
            ),
        )
        movie_data = response.parsed

        # Open 3 equal visual layout zones
        col1, col2, col3 = st.columns(3, gap="large")
        columns = [col1, col2, col3]
        
        for i, movie in enumerate(movie_data.movies[:3]):
            poster_url = get_movie_poster(movie.title, movie.year)
            search_query = urllib.parse.quote(f"where to watch {movie.title} {movie.year}")
            google_search_url = f"https://www.google.com/search?q={search_query}"
            
            with columns[i]:
                with st.container(border=True):
                    st.image(poster_url, use_container_width=True)
                    
                    st.markdown(f"<h3 style='margin-top:15px; margin-bottom:5px; font-weight:800; color:#FFF; font-size:1.5rem; letter-spacing:-0.5px;'>{movie.title}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>🗓️ Year: {movie.year} &nbsp;|&nbsp; <span style='color:#00F0FF; font-weight:600;'>⭐ Match: {movie.rating}/10</span></p>", unsafe_allow_html=True)
                    
                    st.link_button("🔍 Streaming Options", google_search_url, use_container_width=True)
                    st.write("")
                    
                    st.markdown("<p style='color:#FF2E93; font-weight:600; margin-bottom:8px; font-size:0.95rem; text-transform:uppercase; letter-spacing:0.5px;'>🎯 Why It Fits:</p>", unsafe_allow_html=True)
                    st.write(movie.why_it_fits)

    st.write("")
    st.write("---")
    
    # Back navigation array to cleanly dump active session metrics
    if st.button("⬅️ Return to Lounge", use_container_width=True):
        st.session_state.page = "input_page"
        st.session_state.saved_mood = ""
        st.rerun()
