import streamlit as st
import tempfile
import os

# Import fonetizer functions
from fonetizer import parse_input_line, process_phrase, build_excel_table

# Version and copyright
VERSION = "1.0.0"
COPYRIGHT = "© 2025 Laura Mardones"

# Page config
st.set_page_config(
    page_title="Fonetizer - Singing Phonetics for Barbershop",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for better mobile experience
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
    }
    .phrase-counter {
        font-size: 1.2em;
        font-weight: bold;
        color: #1f77b4;
    }
    .copyright {
        text-align: center;
        color: #666;
        font-size: 0.9em;
        margin-top: 2em;
    }
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🎵 Fonetizer")
    st.caption("Fonetiska tabeller för barbershopkvartetter")
with col2:
    st.caption(f"v{VERSION}")

# About section in sidebar
with st.sidebar:
    st.header("Om Fonetizer")
    st.markdown(f"""
    **Fonetizer** är ett verktyg för att skapa fonetiska tabeller från låttexter,
    optimerade för barbershopsång.

    **Utvecklad av:** Laura Mardones
    **Version:** {VERSION}
    {COPYRIGHT}

    ---

    **Teknologi:**
    - Python 3.12
    - Streamlit
    - CMU Pronouncing Dictionary
    - OpenPyXL
    """)

    st.markdown("---")
    st.markdown("**Licens:** MIT License")

# Quick instructions (always visible, compact)
st.info("💡 **Snabbguide:** Skriv text på varje rad. Taktnummer är valfritt. Exempel: `29 When the day is through` eller bara `When the day is through`.")

# Default example for placeholder
example_placeholder = """Exempel:
29 When the day is through,
31 I suffer no,
32 no regrets. know that he who frets,
35 loses the, loses the night.
37 For only a fool,
39 thinks he can hold back the dawn"""

# Session state for text and generated file
if 'text_input_key' not in st.session_state:
    st.session_state.text_input_key = 0
if 'generated_excel' not in st.session_state:
    st.session_state.generated_excel = None

# Main input area
col1, col2 = st.columns([5, 1])
with col1:
    st.subheader("1. Klistra in och redigera text")
with col2:
    st.write("")  # Spacing
    if st.button("🔄 Börja om", use_container_width=True):
        # Increment key to create a new text_area widget (this clears it)
        st.session_state.text_input_key += 1
        st.session_state.generated_excel = None
        st.rerun()

text_input = st.text_area(
    "Text:",
    height=300,
    placeholder=example_placeholder,
    help="Skriv eller klistra in din text här. Taktnummer är valfritt.",
    key=f"text_area_{st.session_state.text_input_key}",
    label_visibility="collapsed"
)

# Clear generated file when text changes
if text_input and st.session_state.generated_excel is not None:
    if text_input != st.session_state.generated_excel.get('source_text', ''):
        st.session_state.generated_excel = None

# Apply button (mobile-friendly)
if st.button("✓ Tillämpa ändringar", use_container_width=True, type="secondary"):
    # Force re-render to apply changes
    st.rerun()

# Real-time validation and preview
lines = [line.strip() for line in text_input.split('\n') if line.strip()]

# Parse and validate
valid_lines = 0
error_lines = []

for idx, line in enumerate(lines, 1):
    try:
        start, text = parse_input_line(line)
        valid_lines += 1
    except ValueError:
        error_lines.append((idx, line))

# Status display - only show if there are errors
st.subheader("2. Status")

if lines:
    # Show errors if any
    if error_lines:
        st.error(f"⚠️ {len(error_lines)} rad(er) med fel:")
        for idx, line in error_lines:
            st.write(f"**Rad {idx}:** {line[:60]}{'...' if len(line) > 60 else ''}")
        st.caption("💡 Varje rad ska innehålla text. Taktnummer är valfritt (t.ex. `29 When the day...` eller bara `When the day...`)")
    else:
        st.success(f"✅ {valid_lines} fraser redo att generera!")
else:
    st.info("Klistra in text i rutan ovan för att komma igång.")

# Generate and download section
st.subheader("3. Ange filnamn och generera")

# Filename input
filename = st.text_input(
    "Filnamn:",
    value="fonetisk_tabell.xlsx",
    help="Namnet på den genererade Excel-filen"
)

# Ensure .xlsx extension
if filename and not filename.endswith('.xlsx'):
    filename += '.xlsx'

# Check if we can generate
can_generate = valid_lines > 0 and len(error_lines) == 0

if not can_generate and lines:
    st.warning("⚠️ Rätta felen innan du kan generera tabellen")

# Show generate button if file not yet generated OR if text has changed
if st.session_state.generated_excel is None:
    # Generate button
    generate_clicked = st.button(
        "🎵 Generera tabell",
        type="primary",
        use_container_width=True,
        disabled=not can_generate
    )

    if generate_clicked and can_generate:
        with st.spinner("🎵 Genererar tabell..."):
            try:
                # Parse all phrases
                phrases = []
                for line in lines:
                    try:
                        start, text = parse_input_line(line)
                        syllables = process_phrase(text)
                        phrases.append((start, syllables))
                    except ValueError as e:
                        st.error(f"❌ Fel i rad: {line}")
                        st.stop()

                # Generate Excel in memory
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    tmp_path = tmp.name

                # Build Excel file (after closing the temp file)
                build_excel_table(phrases, tmp_path)

                # Read the file into memory
                with open(tmp_path, 'rb') as f:
                    excel_data = f.read()

                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except PermissionError:
                    pass

                # Store in session state with current filename and source text
                st.session_state.generated_excel = {
                    'data': excel_data,
                    'filename': filename,
                    'phrase_count': len(phrases),
                    'source_text': text_input
                }

                st.balloons()
                st.rerun()

            except Exception as e:
                st.error(f"❌ Ett fel uppstod vid generering: {str(e)}")
                st.exception(e)

# Show download button if file has been generated
else:
    st.success(f"✅ Tabell genererad med {st.session_state.generated_excel['phrase_count']} fraser!")

    st.download_button(
        label="📥 Ladda ner filen",
        data=st.session_state.generated_excel['data'],
        file_name=st.session_state.generated_excel['filename'],
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        type="primary"
    )

    st.info("💡 Tryck '🔄 Börja om' för att skapa en ny tabell")

# Footer
st.divider()
st.markdown(
    f'<div class="copyright">Fonetizer v{VERSION} - Utvecklad för barbershopkvartetter 🎶<br>{COPYRIGHT}</div>',
    unsafe_allow_html=True
)
