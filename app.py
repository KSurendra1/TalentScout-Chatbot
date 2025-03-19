import streamlit as st
from langchain_groq import ChatGroq

# place with a valid API Key from Groq
GROQ_API_KEY = "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"

# Initialize the ChatGroq LLM model
llm = ChatGroq(
    model="mixtral-8x7b-32768",  # A supported model
    temperature=0.5,
    max_tokens=500,
    timeout=10,
    max_retries=2,
    api_key=GROQ_API_KEY,
)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Define interview questions
questions = [
    {"key": "full_name", "question": "What is your full name?"},
    {"key": "email", "question": "What is your email address?"},
    {"key": "phone", "question": "What is your phone number?"},
    {"key": "experience", "question": "How many years of experience do you have?"},
    {"key": "position", "question": "What position are you applying for?"},
    {"key": "location", "question": "What is your current location?"},
    {"key": "tech_stack", "question": "What technologies do you specialize in?"},
]

#  **Display Chat History**
st.title("🤖 TalentScout Chatbot")
for chat in st.session_state.chat_history:
    role, text = chat
    st.chat_message(role).write(text)

# **Ask the current question**
if st.session_state.current_question < len(questions):
    question = questions[st.session_state.current_question]["question"]
    key = questions[st.session_state.current_question]["key"]

    user_response = st.chat_input(question)

    if user_response:
        # Save response & move to the next question
        st.session_state.answers[key] = user_response
        st.session_state.chat_history.append(("user", user_response))

        st.session_state.current_question += 1

        if st.session_state.current_question < len(questions):
            next_question = questions[st.session_state.current_question]["question"]
            st.session_state.chat_history.append(("assistant", next_question))
        else:
            st.session_state.chat_history.append(("assistant", "Thank you! Generating interview questions..."))
        
        st.experimental_rerun()

#  **After all questions, generate technical interview questions**
if st.session_state.current_question == len(questions):
    tech_stack = st.session_state.answers["tech_stack"]
    
    # Display summary
    st.subheader(" Your Profile Summary")
    for q in questions:
        st.write(f"- **{q['question']}** {st.session_state.answers[q['key']]}")

    # Generate technical questions based on tech stack
    prompt = f"You are an interviewer. Generate 3-5 technical interview questions for the following tech stack: {tech_stack}."

    try:
        with st.spinner("Generating technical questions..."):
            response = llm.invoke([("system", prompt)])
            interview_questions = response.content
            st.session_state.chat_history.append(("assistant", interview_questions))
            st.chat_message("assistant").write(interview_questions)
    except Exception as e:
        st.error(f"Error: Unable to generate questions. {str(e)}")

    #  Restart Button
    if st.button("🔄 Restart"):
        st.session_state.chat_history = []
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.experimental_rerun()
