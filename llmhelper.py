from langchain import PromptTemplate, LLMChain
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.llms import AzureOpenAI

from loaderhelper import get_chroma_db


class LangchainHelper:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.db = get_chroma_db(module_name)
        self.llm = AzureOpenAI(
            deployment_name="text-davinci-003",
            model_name="text-davinci-003",
            temperature=0,
            max_tokens=1024,
        )

    def _create_llm_chain(self):
        prompt_template = """
            As a GitHub repository owner for a project called """ + self.module_name + """, I have received an issue with the following details:
            
            Issue title: {issue_title}
            Issue comment: {issue_comment}
            Context: {context}
            
            Based on the information provided, please find below my response, code examples or corrections, explanation, and resources used. This response will be posted directly on GitHub.
            
            Title: {issue_title}
            Response:
            
            {response}
            Code example or correction:
            
            {code_example_or_correction}
            Explanation:
            {explanation}
            
            Resources used:
            {resources_used}
        """

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "issue_title", "issue_comment"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain

    def initialize_chat_bot(self):
        conversational_chain = ConversationalRetrievalChain.from_llm(self.llm, self.db.as_retriever())
        return conversational_chain

    def assist_github_issue(self, issue_title, issue_comment):
        context = ""
        chain = self._create_llm_chain()
        documents = self.db.similarity_search(query=issue_title, k=4)
        for doc in documents:
            context += doc.page_content
        inputs = [
            {"context": context, "issue_title": issue_title, "issue_comment": issue_comment}
        ]
        return chain.apply(inputs)

    def answer_simple_question(self, query: str):
        retrieval_qa = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.db.as_retriever())
        return retrieval_qa.run(query)
