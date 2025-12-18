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
st.info("💡 **Snabbguide:** Skriv taktnummer + mellanslag + text på varje rad. Exempel: `29 When the day is through,`")

# Example loading buttons
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    load_example = st.button("📝 Ladda exempel", use_container_width=True)
with col2:
    clear_text = st.button("🗑️ Rensa", use_container_width=True)

# Default and example texts
example_text = """29 When the day is through,
31 I suffer no,
32 no regrets. know that he who frets,
35 loses the, loses the night.
37 For only a fool,
39 thinks he can hold back the dawn"""

# Handle button clicks
if 'text_content' not in st.session_state:
    st.session_state.text_content = example_text

if load_example:
    st.session_state.text_content = example_text
    st.rerun()

if clear_text:
    st.session_state.text_content = ""
    st.rerun()

# Main input area
st.subheader("1. Klistra in och redigera text")

text_input = st.text_area(
    "Text:",
    value=st.session_state.text_content,
    height=300,
    placeholder="Exempel:\n29 When the day is through,\n31 I suffer no,\n32 no regrets...",
    help="Format: TAKTNUMMER MELLANSLAG TEXT\nVarje rad = en fras",
    key="text_area"
)

# Update session state
st.session_state.text_content = text_input

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

# Status display
st.subheader("2. Status")

if lines:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📝 Totalt fraser", len(lines))
    with col2:
        st.metric("✅ Korrekta", valid_lines)
    with col3:
        st.metric("❌ Fel", len(error_lines))

    # Show errors if any
    if error_lines:
        with st.expander("⚠️ Visa fel", expanded=True):
            for idx, line in error_lines:
                st.error(f"**Rad {idx}:** {line[:60]}{'...' if len(line) > 60 else ''}")
            st.caption("💡 Rätt format: `NUMMER mellanslag TEXT` (t.ex. `29 When the day...`)")
else:
    st.warning("Ingen text att bearbeta. Klistra in text eller ladda exempel.")

# Generate button
st.subheader("3. Generera fonetisk tabell")

col1, col2 = st.columns([2, 2])

with col1:
    filename = st.text_input(
        "Filnamn:",
        value="fonetisk_tabell.xlsx",
        help="Namnet på den genererade Excel-filen"
    )

    # Ensure .xlsx extension
    if filename and not filename.endswith('.xlsx'):
        filename += '.xlsx'

with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing

# Generate button (disabled if there are errors)
can_generate = valid_lines > 0 and len(error_lines) == 0

if not can_generate and lines:
    st.warning("⚠️ Rätta felen innan du genererar tabellen")

generate_button = st.button(
    "🎵 Generera fonetisk tabell",
    type="primary",
    use_container_width=True,
    disabled=not can_generate
)

if generate_button:
    if not lines:
        st.error("❌ Ingen text att bearbeta!")
    else:
        with st.spinner("🎵 Bearbetar text och genererar tabell..."):
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
                    pass  # Windows sometimes holds the file, it will be cleaned up later

                st.success(f"✅ Fonetisk tabell genererad! ({len(phrases)} fraser)")

                # Download button
                st.download_button(
                    label="📥 Ladda ner Excel-fil",
                    data=excel_data,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    type="primary"
                )

                st.balloons()

            except Exception as e:
                st.error(f"❌ Ett fel uppstod: {str(e)}")
                st.exception(e)

# Footer
st.divider()
st.markdown(
    f'<div class="copyright">Fonetizer v{VERSION} - Utvecklad för barbershopkvartetter 🎶<br>{COPYRIGHT}</div>',
    unsafe_allow_html=True
)
