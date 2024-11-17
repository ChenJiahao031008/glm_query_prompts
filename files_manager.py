from common import public, private
import os
import re

class FilesManager:
    def __init__(self):
        self.qa_knowledges = {}
        self.des_knowledges = []

    @public
    def GetAllKnowledgesList(self):
        all_knowledges = []
        for qus, ans in self.qa_knowledges.items():
            all_knowledges.append("question: " + qus + "\nanswer: " + ans)
        all_knowledges = all_knowledges + self.des_knowledges
        return all_knowledges

    @public
    def RunDirectoryRead(self, directory, verbose=True):
        for entry in os.listdir(directory):
            file_path = os.path.join(directory, entry)
            if os.path.isfile(file_path) and self._IsDesignatedFile(file_path, ".md"):
                self._ReadMarkdownFile(file_path, verbose)

    @private
    def _ReadMarkdownFile(self, file_path, verbose=True):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            qa_dict = self._ExtractQuestionsAnswers(content)
            self.qa_knowledges.update(qa_dict)
        if verbose:
            self._PrintInfos()

    @private
    def _ExtractQuestionsAnswers(self, text):
        qa_dict = {}
        pattern = re.compile(r"## (.*?)\n(.*?)(?=\n##)", re.DOTALL)
        matches = pattern.findall(text)
        for title, content in matches:
            title = title.strip()
            answer = self._RemoveEmptyLines(content.strip())
            qa_dict[title] = answer
        return qa_dict

    @private
    def _IsDesignatedFile(self, file_name, suffix=".md"):
        _, ext = os.path.splitext(file_name)
        return ext.lower() == suffix

    @private
    def _PrintInfos(self):
        for title, answer in self.qa_knowledges.items():
            print(f"Q:** {title}")
            print(f"A:** {answer}")

    @private
    def _RemoveEmptyLines(self, text):
        return "\n".join([line for line in text.splitlines() if line.strip()])
