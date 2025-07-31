import os
import streamlit as st
from crewai import Agent, Task, Crew

# ---------- Page Configuration ----------
st.set_page_config(page_title="✨ AI Blog Creator", page_icon="🧠", layout="centered")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #2c3e50;
        color: white;
        border: 1px solid #16a085;
        padding: 0.5rem;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #16a085;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
    }
    .stMarkdown h1 {
        color: #1abc9c;
        text-align: center;
    }
    .glass {
        background: rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header & Visual ----------
st.image("Technology.gif", width=300, use_column_width=False)
st.markdown("<h1 class='glass'>🚀 Generate Beautiful AI-Powered Blogs Instantly</h1>", unsafe_allow_html=True)

# ---------- Input Section ----------
with st.container():
    topic = st.text_input("🧠 Enter a topic for your blog:", placeholder="e.g., The Future of AI in Healthcare")
    submit = st.button("✨ Generate Blog Post")

# ---------- CrewAI Logic ----------
def run_crewai(topic):
    os.environ["OPENAI_MODEL_NAME"] = "mistral-small"
    os.environ["OPENAI_API_KEY"] = "v2bSyVDhF5amgebJyUfRwNmVJeszm8Ta"
    os.environ["OPENAI_API_BASE"] = "https://api.mistral.ai/v1"

    planner = Agent(
        role="Content Planner",
        goal=f"Plan engaging and factually accurate content on {topic}",
        backstory=f"You're planning a blog about {topic}.",
        allow_delegation=False,
        verbose=False,
    )

    writer = Agent(
        role="Content Writer",
        goal=f"Write insightful and accurate opinion pieces about the topic: {topic}",
        backstory="You're a blog writer basing your writing on the planner's outline.",
        allow_delegation=False,
        verbose=False,
    )

    editor = Agent(
        role="Editor",
        goal="Edit and polish the blog post.",
        backstory="You're responsible for making sure the post reads well.",
        allow_delegation=False,
        verbose=False,
    )

    plan = Task(
        description=(
            "Research the latest trends and generate a structured content outline "
            "with SEO keywords and clear structure."
        ),
        expected_output="Outline with audience insights, structure, SEO, and references.",
        agent=planner,
    )

    write = Task(
        description=(
            "Create a compelling blog using the outline with engaging headings, "
            "body sections, and a strong conclusion. Ensure natural use of SEO terms."
        ),
        expected_output="Markdown-formatted blog post, 2-3 paragraphs per section.",
        agent=writer,
    )

    edit = Task(
        description="Polish the final blog and ensure consistency and clarity.",
        expected_output="Cleaned markdown blog post ready to publish.",
        agent=editor,
    )

    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        verbose=2,
    )

    return crew.kickoff(inputs={"topic": topic})

# ---------- Blog Generation ----------
if submit:
    if not topic.strip():
        st.warning("⚠️ Please enter a topic to generate the blog.")
        st.stop()

    with st.spinner("💡 Crafting your personalized blog..."):
        try:
            blog = run_crewai(topic)
            st.balloons()
            st.markdown("## ✅ Here's your beautifully generated blog:")
            st.markdown(blog, unsafe_allow_html=True)

            st.download_button(
                "📥 Download Blog",
                blog,
                file_name=f"{topic.replace(' ', '_')}_blog.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error("❌ An error occurred while generating your blog.")
            st.exception(e)
