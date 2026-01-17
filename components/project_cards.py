# components/project_cards.py
# Reusable project cards with modal dialog for details

from __future__ import annotations
import textwrap
import streamlit as st

# --- one-time CSS for tag badges and image masks ---
def _ensure_css():
    if st.session_state.get("_project_cards_css_loaded"):
        return
    st.session_state["_project_cards_css_loaded"] = True
    st.markdown(
        """
        <style>
        .tag {
            display: inline-block;
            padding: 2px 8px;
            margin-right: 6px;
            margin-bottom: 6px;
            border-radius: 999px;
            background: #111827;
            color: #e5e7eb;
            font-size: 11px;
            border: 1px solid #374151;
        }
        .card-cover {
            overflow: hidden;
            border: 1px solid var(--secondary-background-color,#2a2a2a);
        }
        .card-cover img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def _truncate(text: str, width: int = 140) -> str:
    txt = " ".join(text.strip().split())
    return textwrap.shorten(txt, width=width, placeholder="...")

def _tag_row(tags: list[str] | None) -> None:
    if not tags:
        return
    st.markdown(
        " ".join([f"<span class='tag'>{t}</span>" for t in tags]),
        unsafe_allow_html=True,
    )

def _image_cover(src: str, height: int = 220, radius: int = 14):
    # Replace CSS variables with real numbers to keep things fast
    html = (
        f'<div class="card-cover" style="height:{height}px; border-radius:{radius}px;">'
        f'<img src="{src}" />'
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)

@st.dialog("Project details")
def _show_dialog(project: dict, *, modal_image_height: int = 340):
    _image_cover(project["image"], height=modal_image_height, radius=16)
    st.markdown(f"### {project['title']}")
    _tag_row(project.get("tags", []))
    st.write("")
    st.markdown(project["description"])
    links = project.get("links") or {}
    if links:
        st.write("")
        st.markdown("#### Links")
        for name, url in links.items():
            if url:
                st.markdown(f"- [{name}]({url})")

def render_project_card(
    project: dict,
    *,
    key: str,
    summary_width: int = 200,
    cover_height: int = 220,
    radius: int = 14,
    button_label: str = "View details",
) -> None:
    """Render a single project card inside the current container."""
    _ensure_css()
    with st.container(border=True):
        _image_cover(project["image"], height=cover_height, radius=radius)
        st.markdown(f"**{project['title']}**")
        _tag_row(project.get("tags", []))
        st.caption(_truncate(project["summary"], summary_width))
        open_key = f"open_{project['slug']}_{key}"
        if st.button(button_label, key=open_key, width='stretch'):
            _show_dialog(project)

def render_project_grid(
    projects: list[dict],
    *,
    cols_per_row: int = 2,
    summary_width: int = 200,
    cover_height: int = 220,
    radius: int = 14,
    button_label: str = "View details",
) -> None:
    """Render a responsive grid of project cards."""
    _ensure_css()
    # slice into rows
    rows = [projects[i:i + cols_per_row] for i in range(0, len(projects), cols_per_row)]
    for r_index, row in enumerate(rows):
        cols = st.columns(cols_per_row)
        for c_index, proj in enumerate(row):
            with cols[c_index]:
                render_project_card(
                    proj,
                    key=f"{r_index}_{c_index}",
                    summary_width=summary_width,
                    cover_height=cover_height,
                    radius=radius,
                    button_label=button_label,
                )