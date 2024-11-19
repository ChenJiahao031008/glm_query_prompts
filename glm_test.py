from common import *
from files_manager import FilesManager
from glm_interface import GLMInterface
from prompt_template import PromptTemplate

def main():
    files_manager = FilesManager()
    files_manager.RunDirectoryRead(directory, False)

    ai_interface = GLMInterface(zhipuai_api_key)
    ai_interface.CreateKnowledgeBase(files_manager.GetAllKnowledgesList())

    prompt_template = PromptTemplate()
    system_prompt = prompt_template.GetSystemPrompt()

    query_text = "介绍下单目尺度漂移。"
    knowledges = ai_interface.QueryKnowledgeBase(query_text, k=3, verbose=False)
    qa_prompt = prompt_template.GetQAPrompt(query_text, knowledges)
    response = ai_interface.SendMessagesWithSystem(system_prompt, qa_prompt)

    query_text = "双目会有尺度漂移吗?"
    knowledges = ai_interface.QueryKnowledgeBase(query_text, k=3, verbose=False)
    qa_prompt = prompt_template.GetQAPrompt(query_text, knowledges)
    response = ai_interface.SendMessagesWithSystem(system_prompt, qa_prompt)

if __name__ == "__main__":
    main()
