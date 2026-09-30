from langchain_core.prompts import PromptTemplate


programming_prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a programming assistant. Answer this coding question clearly:\n\n{question}"
)


math_prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a math assistant. Solve this math problem step by step:\n\n{question}"
)


english_prompt = PromptTemplate(
    input_variables=["question"],
    template="You are an English language assistant. Answer this English/language question clearly:\n\n{question}"
)


general_prompt = PromptTemplate(
    input_variables=["question"],
    template="You are a general subject assistant. Answer this general question clearly:\n\n{question}"
)



summary_prompt = PromptTemplate(
    input_variables=["question"],
    template="Summarize the answer to this question in one or two sentences:\n\n{question}"
)
