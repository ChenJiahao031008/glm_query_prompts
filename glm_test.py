from common import *
from files_manager import FilesManager
from glm_interface import GLMInterface

def main():
    files_manager = FilesManager()
    files_manager.RunDirectoryRead(directory, False)
    ai_interface = GLMInterface(zhipuai_api_key)
    ai_interface.CreateKnowledgeBase(files_manager.GetAllKnowledgesList())
    query_text = "介绍下单目尺度漂移"
    ai_interface.QueryKnowledgeBase(query_text)


if __name__ == "__main__":
    main()
