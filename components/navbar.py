# components/navbar.py
import os
import streamlit as st

def render_sidebar_profile(*, show_env: bool = False) -> None:
    """Sidebar profile block that works with Streamlit default navigation."""
    st.markdown("## Sanket Shah")
    st.image(
        "https://avatars.githubusercontent.com/u/68991626?v=4",
        caption="Sanket Shah",
        use_container_width=True,
    )
    st.caption("Data Scientist • ML Engineer • Gen AI")
    st.write("")

    # Optional quick links
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("GitHub", "https://github.com/Sanket0412", use_container_width=True)
    with c2:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/sanket0412/", use_container_width=True)

    # if show_env:
    #     st.divider()
    #     st.caption("Environment")
    #     st.write(f"Mode: {os.getenv('APP_ENV', 'development')}")
    #     st.write(f"Model: {os.getenv('MODEL_NAME', 'gpt-4o-mini')}")
