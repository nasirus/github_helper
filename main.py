import logging

import llmhelper

bot_mode = "chat"
chat_history = []
module_name = "langchain"
question = "what is langchain ?"

if bot_mode == "chat":
    chat_bot = llmhelper.LangchainHelper(module_name=module_name).initialize_chat_bot()
    print(f"Start chat with {module_name}, type your question")

    logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s %(levelname)s %(message)s')

    while True:
        query = input("-->")
        result = chat_bot({"question": query, "chat_history": chat_history})
        chat_history.append((query, result["answer"]))
        print(result["answer"] + " |chat_history : " + str(len(chat_history)))
elif bot_mode == "qa":
    langchain_helper = llmhelper.LangchainHelper(module_name=module_name)
    resul = langchain_helper.answer_simple_question(query=question)
    print(resul)
