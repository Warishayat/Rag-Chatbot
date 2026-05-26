from langchain_core.prompts import ChatPromptTemplate

def prompt_templete():
    return ChatPromptTemplate.from_template(
        """
        You are an intelligent assistant.

        Answer ONLY using the provided context.

        Context:
        {context}

        User Question:
        {question}

        Rules:
        - Give a clear and concise answer.
        - If answer is not found in context, say:
          "I could not find this information in the document."
        - Do not hallucinate.
        """
    )