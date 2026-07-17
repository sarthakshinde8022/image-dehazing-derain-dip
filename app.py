"""
Shared visual theme for the DIP mini project app.
Call inject_custom_css() near the top of every page, right after
st.set_page_config().

Design concept ("Clarity"): the visual language of haze lifting to
reveal a clear scene. A deep atmospheric navy grounds the page; a cool
teal marks the moment of restoration; warm gold is used sparingly for
emphasis, like sun breaking through.
"""

import streamlit as st

BG_DEEP = "#0F1620"
BG_PANEL = "#1B2430"
FOG = "#8FA3B0"
CLARITY = "#4FD1C5"
SUNBREAK = "#E3B23C"
TEXT_PRIMARY = "#EAF2F5"
TEXT_MUTED = "#93A5B1"


def inject_custom_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {{
            font-family: 'IBM Plex Sans', sans-serif;
        }}

        h1, h2, h3 {{
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.01em;
        }}

        code {{
            font-family: 'IBM Plex Mono', monospace !important;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        .clarity-divider {{
            height: 3px;
            border: none;
            border-radius: 2px;
            margin: 1.75rem 0;
            background: linear-gradient(90deg, {FOG} 0%, {CLARITY} 60%, {SUNBREAK} 100%);
            opacity: 0.85;
        }}

        .eyebrow {{
            font-family: 'IBM Plex Mono', monospace;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            font-size: 0.75rem;
            color: {CLARITY};
            margin-bottom: 0.25rem;
        }}

        .stage-card {{
            background: {BG_PANEL};
            border: 1px solid rgba(143, 163, 176, 0.25);
            border-radius: 10px;
            padding: 1.25rem 1.5rem;
            height: 100%;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}
        .stage-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(79, 209, 197, 0.5);
        }}
        @media (prefers-reduced-motion: reduce) {{
            .stage-card {{ transition: none; }}
            .stage-card:hover {{ transform: none; }}
        }}

        .stage-number {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: {CLARITY};
        }}

        .badge {{
            display: inline-block;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.75rem;
            padding: 0.25rem 0.65rem;
            border-radius: 999px;
            border: 1px solid rgba(79, 209, 197, 0.4);
            color: {CLARITY};
            margin: 0 0.35rem 0.35rem 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
