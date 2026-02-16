# components/project_cards.py
# Reusable project cards with modal dialog for details

from __future__ import annotations

import textwrap
from typing import Any, Dict, List, Optional

import streamlit as st

import base64
import mimetypes
import os
from pathlib import Path

# =========================
# CSS (loaded once)
# =========================
def _ensure_css() -> None:
    if st.session_state.get("_project_cards_css_loaded"):
        return
    st.session_state["_project_cards_css_loaded"] = True

    st.markdown(
        """
        <style>
        /* Softer, cleaner chips */
        .tag {
            display: inline-flex;
            align-items: center;
            padding: 3px 10px;
            border-radius: 999px;
            background: rgba(17, 24, 39, 0.55);
            color: #e5e7eb;
            font-size: 12px;
            border: 1px solid rgba(55, 65, 81, 0.7);
            letter-spacing: 0.2px;
            line-height: 1.2;
            white-space: nowrap;
            margin: 0;
        }

        .tag-muted {
            background: rgba(17, 24, 39, 0.35);
            border: 1px solid rgba(55, 65, 81, 0.5);
            color: rgba(229, 231, 235, 0.95);
        }

        .tags-wrap {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 6px;
            margin-bottom: 6px;
        }

        /* Image mask, guaranteed no overflow */
        .card-cover {
            width: 100%;
            overflow: hidden;
            box-sizing: border-box;
            border: 1px solid var(--secondary-background-color, #2a2a2a);
        }

        .card-cover img {
            width: 100% !important;
            max-width: 100% !important;
            height: 100% !important;
            display: block !important;
            object-fit: cover !important;
        }

        /* Dialog section helpers */
        .meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 6px;
            margin-bottom: 4px;
            color: rgba(229, 231, 235, 0.9);
            font-size: 13px;
        }

        .meta-pill {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid rgba(55, 65, 81, 0.55);
            background: rgba(17, 24, 39, 0.25);
        }

        .hr-soft {
            height: 1px;
            background: rgba(55, 65, 81, 0.35);
            border: 0;
            margin: 14px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =========================
# Helpers
# =========================
def _truncate(text: str, width: int = 140) -> str:
    txt = " ".join((text or "").strip().split())
    if not txt:
        return ""
    return textwrap.shorten(txt, width=width, placeholder="...")


def _as_list(v: Any) -> List[str]:
    if not v:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    if isinstance(v, str):
        return [x.strip() for x in v.split(",") if x.strip()]
    return [str(v)]


def _tag_row(tags: Optional[List[str]] = None, *, muted: bool = False) -> None:
    tags = tags or []
    if not tags:
        return

    # Inline styles so it renders correctly inside st.dialog as well (DOM differs vs main page)
    bg = "rgba(17, 24, 39, 0.35)" if muted else "rgba(17, 24, 39, 0.55)"
    border = "rgba(55, 65, 81, 0.5)" if muted else "rgba(55, 65, 81, 0.7)"
    color = "rgba(229, 231, 235, 0.95)" if muted else "#e5e7eb"

    chip_style = (
        f"display:inline-flex;align-items:center;"
        f"padding:3px 10px;border-radius:999px;"
        f"background:{bg};color:{color};font-size:12px;"
        f"border:1px solid {border};letter-spacing:0.2px;"
        f"line-height:1.2;white-space:nowrap;"
        f"margin:0;"
    )

    # Use a flex wrapper with gap, plus a small non-breaking spacer as a hard fallback
    html = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin-top:6px;margin-bottom:6px;'>"
    html += "".join([f"<span style=\"{chip_style}\">{t}</span>" for t in tags])
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)



def _image_cover(src: str, *, height: int = 220, radius: int = 14) -> None:
    # Supports both:
    # 1) Remote URLs (https://...)
    # 2) Local repo paths like "content/covers/ECHOS2.png" by embedding as data URI
    final_src = src

    try:
        if src and not src.lower().startswith(("http://", "https://", "data:")):
            local_path = Path(src)
            if local_path.exists() and local_path.is_file():
                mime, _ = mimetypes.guess_type(str(local_path))
                if not mime:
                    mime = "image/png"
                b64 = base64.b64encode(local_path.read_bytes()).decode("utf-8")
                final_src = f"data:{mime};base64,{b64}"
    except Exception:
        final_src = src

    html = f"""
    <div class="card-cover" style="height:{height}px; border-radius:{radius}px;">
        <img
            src="{final_src}"
            style="border-radius:{radius}px; width:100%; max-width:100%; height:100%; object-fit:cover; display:block;"
        />
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)



def _safe_get(project: Dict[str, Any], key: str, default: Any = None) -> Any:
    return project.get(key, default)


def _render_links(links: Dict[str, str]) -> None:
    if not links:
        return
    st.markdown("#### Links")
    for name, url in links.items():
        if url:
            st.markdown(f"- [{name}]({url})")


def _render_dialog_tech_stack(project: Dict[str, Any]) -> None:
    tech = _as_list(_safe_get(project, "tech", []))
    if not tech:
        # Backward compatible: if you only have tags, reuse them as "Tech stack" chips in the dialog
        tech = _as_list(_safe_get(project, "tags", []))
    if not tech:
        return

    st.markdown("#### Tech stack")
    _tag_row(tech, muted=True)


def _render_dialog_meta(project: Dict[str, Any]) -> None:
    # Optional fields you can add later in PROJECTS:
    # - "role": "Data Scientist"
    # - "domain": "Ads / Audience Intelligence"
    # - "impact": ["Reduced X from Y to Z", "Saved N hours/week"]
    role = str(_safe_get(project, "role", "") or "").strip()
    domain = str(_safe_get(project, "domain", "") or "").strip()

    pills: List[str] = []
    if role:
        pills.append(f"<span class='meta-pill'>Role: {role}</span>")
    if domain:
        pills.append(f"<span class='meta-pill'>Domain: {domain}</span>")

    if pills:
        st.markdown("<div class='meta-row'>" + "".join(pills) + "</div>", unsafe_allow_html=True)

    impact = _as_list(_safe_get(project, "impact", []))
    if impact:
        st.markdown("#### Impact")
        for it in impact:
            st.markdown(f"- {it}")


# =========================
# Dialog (details)
# =========================
@st.dialog("Project details")
def _show_dialog(project: Dict[str, Any], *, modal_image_height: int = 340) -> None:
    _ensure_css()

    image = str(_safe_get(project, "image", "") or "").strip()
    if image:
        _image_cover(image, height=modal_image_height, radius=16)

    title = str(_safe_get(project, "title", "") or "").strip()
    if title:
        st.markdown(f"### {title}")

    _render_dialog_meta(project)

    tags = _as_list(_safe_get(project, "tags", []))
    _tag_row(tags)

    st.markdown("<hr class='hr-soft'/>", unsafe_allow_html=True)

    _render_dialog_tech_stack(project)

    description = str(_safe_get(project, "description", "") or "")
    if description.strip():
        st.markdown("#### Overview")
        st.markdown(description)

    links = _safe_get(project, "links", {}) or {}
    if isinstance(links, dict) and links:
        st.markdown("<hr class='hr-soft'/>", unsafe_allow_html=True)
        _render_links(links)


# =========================
# Cards + Grid (responsive)
# =========================
def _compute_cols_per_row(default_cols: int = 2) -> int:
    # Responsive behavior without hover effects:
    # - narrow viewport: 1
    # - medium: default_cols
    # - wide: default_cols + 1 (capped at 3)
    try:
        vw = int(st.session_state.get("_viewport_width", 0) or 0)
    except Exception:
        vw = 0

    if vw <= 0:
        return max(1, min(3, default_cols))

    if vw < 900:
        return 1
    if vw < 1350:
        return max(1, min(3, default_cols))
    return max(1, min(3, default_cols + 1))


def _inject_viewport_probe() -> None:
    # Tiny JS probe to store viewport width in session_state via query params
    # Works safely without needing hover, and makes the grid feel responsive.
    st.markdown(
        """
        <script>
        (function() {
            try {
                const w = window.innerWidth || document.documentElement.clientWidth || 0;
                const url = new URL(window.location.href);
                const prev = url.searchParams.get("_vw");
                if (String(prev) !== String(w)) {
                    url.searchParams.set("_vw", String(w));
                    window.history.replaceState({}, "", url.toString());
                }
            } catch (e) {}
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )

    try:
        q = st.query_params
        vw = q.get("_vw", None)
        if vw:
            st.session_state["_viewport_width"] = int(vw)
    except Exception:
        pass


def render_project_card(
    project: Dict[str, Any],
    *,
    key: str,
    summary_width: int = 200,
    cover_height: int = 220,
    radius: int = 14,
    button_label: str = "View details",
) -> None:
    _ensure_css()

    with st.container(border=True):
        image = str(_safe_get(project, "image", "") or "").strip()
        if image:
            _image_cover(image, height=cover_height, radius=radius)

        st.markdown(f"**{_safe_get(project, 'title', '')}**")

        tags = _as_list(_safe_get(project, "tags", []))
        _tag_row(tags)

        summary = str(_safe_get(project, "summary", "") or "")
        if summary.strip():
            st.caption(_truncate(summary, summary_width))

        open_key = f"open_{_safe_get(project, 'slug', 'project')}_{key}"
        if st.button(button_label, key=open_key, width="stretch"):
            _show_dialog(project)


def render_project_grid(
    projects: List[Dict[str, Any]],
    *,
    cols_per_row: int = 2,
    summary_width: int = 200,
    cover_height: int = 220,
    radius: int = 14,
    button_label: str = "View details",
    responsive: bool = True,
) -> None:
    _ensure_css()

    if responsive:
        _inject_viewport_probe()
        cols_per_row = _compute_cols_per_row(cols_per_row)

    rows = [projects[i : i + cols_per_row] for i in range(0, len(projects), cols_per_row)]
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
