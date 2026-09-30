from langchain_core.runnables import RunnableBranch
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from prompts import programming_prompt, math_prompt, english_prompt, general_prompt, summary_prompt
from langchain_core.runnables import RunnableParallel
from schemas import ResponseSchema

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b")
structured_llm = llm.with_structured_output(ResponseSchema)


def is_programming(input_dict):
    keywords = ["code", "python", "function", "bug", "error", "programming"]
    return any(word in input_dict["question"].lower() for word in keywords)

def is_math(input_dict):
    keywords = ["math", "equation", "geometry", "algebra", "puzzle", "calculus","numbers"]
    return any(word in input_dict["question"].lower() for word in keywords)


def is_english(input_dict):
    keywords = ["english", "literacy", "tense", "grammar", "spelling", "paragraph", "essay"]
    return any(word in input_dict["question"].lower() for word in keywords)


programming_chain = programming_prompt | structured_llm
math_chain = math_prompt | structured_llm
english_chain = english_prompt | structured_llm
general_chain = general_prompt | structured_llm


summary_chain = summary_prompt | structured_llm



branch = RunnableBranch(
    (is_programming, programming_chain),
    (is_math, math_chain),
    (is_english, english_chain),
    general_chain
)



chat_parallel = RunnableParallel(
    answer=branch,
    summary=summary_chain
)


