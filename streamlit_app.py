import streamlit as st
from PIL import Image

import base64
import io

st.title("[shields.io](https://shields.io) badge with custom logo")

logo = st.file_uploader("Upload logo", type=["png", "jpg", "jpeg", "svg"])
st.info("Logo names from [simple-icons](https://github.com/simple-icons/simple-icons/blob/develop/slugs.md).")
logo_text = st.text_input("Logo name (overrides uploaded image)", "default")

badge_text = st.text_input("Badge text (you can seperate with a '-' to get sub-text)", "badge-text")
badge_style = st.selectbox("Badge style", ["flat", "flat-square", "for-the-badge", "plastic", "social"])
badge_color = st.text_input("Badge color", "blue")

badge_width = st.slider("Badge width", 0, 80, 20)

if logo and logo_text == "default":
    if logo.name.endswith(".svg"):
        logo = logo.read().decode("utf-8")
        # svg to png
        import cairosvg
        logo = cairosvg.svg2png(bytestring=logo)
        logo = io.BytesIO(logo)
    

    logo = Image.open(logo)
    resizing_ratio = logo.size[1] / 40

    logo = logo.resize((int(logo.size[0] / resizing_ratio), 40))

    buffered = io.BytesIO()
    logo.save(buffered, format="PNG")
    logo = base64.b64encode(buffered.getvalue()).decode()
    logo = f"data:image/png;base64,{logo}"



badge_url = f"https://img.shields.io/badge/{badge_text}-{badge_color}?&style={badge_style}&logoWidth={badge_width}"
#badge_url = f"https://img.shields.io/badge/{badge_text}-{badge_color}?style={badge_style}"

if logo_text != "default":
    badge_url += f"&logo={logo_text}"
elif logo is not None:
    badge_url += f"&logo={logo}"

st.image(badge_url)

with st.expander("Add links to the image (HTML and Markdown only)"):
    url = st.text_input("URL", "htt://example.com")

markdown_tab, html_tab, url_tab = st.tabs(["Markdown", "HTML", "URL"])

with html_tab:
    st.code(f"""<img src="{badge_url}" alt="{badge_text}">""")
    st.write("Link added:")
    st.code(f"""<a href="{url}"><img src="{badge_url}" alt="{badge_text}"></a>""")

with markdown_tab:
    st.code(f"![{badge_text}]({badge_url})")
    st.write("Link added:")
    st.code(f"[![{badge_text}]({badge_url})]({url})")

with url_tab:
    st.code(badge_url)

