import streamlit as st
from src.search import search
from src.skills import compare

st.set_page_config(page_title="AI Job Recommender", layout="centered")
st.title("AI Job Recommendation System")
st.write("Paste your resume or a short profile, and get matching jobs.")

resume = st.text_area("Your resume / profile", height=220,
                      placeholder="Skills, projects, experience...")

col1, col2 = st.columns(2)
cities = col1.multiselect("Cities (optional)",
                          ["Pune", "Bangalore", "Hyderabad", "Mumbai", "Chennai", "Noida", "Delhi", "Gurgaon"])
max_years = col2.number_input("Max years of experience asked", 0, 15, 15)

if st.button("Find jobs") and resume.strip():
    with st.spinner("Searching..."):
        results = search(resume, k=10, cities=cities or None, max_years=max_years)
    if not results:
        st.warning("No jobs found. Try removing a filter.")
    for r in results:
        matched, missing = compare(resume, r["title_clean"] + " " + r["description"])
        st.subheader(r["title_clean"])
        st.write(f"{r['company']}  |  {r['location']}  |  match {r['score']}")
        if matched:
            st.success("You have: " + ", ".join(matched))
        if missing:
            st.warning("Missing: " + ", ".join(missing))
        if not matched and not missing:
            st.caption("No known skills found in this posting's text.")
        st.link_button("View job", r["url"])
        st.divider()