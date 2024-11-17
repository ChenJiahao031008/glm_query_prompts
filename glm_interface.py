from common import *
import os
import time
import numpy as np
from zhipuai import ZhipuAI
from sklearn.preprocessing import normalize
import numpy as np
import faiss
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable


class EmbeddingInterface:
    def __init__(self, client, dimensions=2048):
        self.model = "embedding-3"
        self.client = client
        self.dimensions = dimensions
        self.knowledge_base = {}
        self.index = faiss.IndexFlatIP(self.dimensions)

    @public
    def ClearKnowledgeBase(self):
        self.knowledge_base = {}

    @public
    def CreateEmbeddings(self, texts):
        embeddings = []
        for text in texts:
            embeddings.append(self.CreateEmbedding(text))
        return np.array(embeddings).reshape(len(embeddings), self.dimensions)

    @public
    def CreateEmbedding(self, text):
        response = self.client.embeddings.create(
            model=self.model, input=[text], dimensions=self.dimensions
        )
        normalized_embeddings = normalize(
            np.array([response.data[0].embedding]).astype("float32")
        )
        return normalized_embeddings

    @public
    def CreateKnowledgeBase(self, all_knowledge):
        embeddings = self.CreateEmbeddings(all_knowledge)

        self.index.add(embeddings)
        assert len(embeddings) == len(all_knowledge)
        for index, embedding in enumerate(embeddings):
            self.knowledge_base[index] = all_knowledge[index]

    @public
    def QueryKnowledgeBase(self, query_text, k=3, verbose = True):
        query_embedding = self.CreateEmbedding(query_text)
        k = min(k, len(self.knowledge_base))
        distances, indices = self.index.search(query_embedding, k)
        if verbose:
            for i, idx in enumerate(indices[0]):
                knowledge = self.knowledge_base[idx]
                print(f"similarity: {distances[0][i]:.4f}\nmatching text: \n{knowledge}\n")


class GLMInterface:
    def __init__(self, zhipuai_api_key, model="glm-4"):
        os.environ["ZHIPUAI_API_KEY"] = zhipuai_api_key
        self.client = ZhipuAI()
        self.model = model
        self.embeddings = EmbeddingInterface(self.client)

    @public
    def SendMessages(self, role="user", prompt=""):
        response = self.client.chat.completions.create(
            semodel=self.model,
            messages=[{"role": self.role, "content": prompt}],
            top_p=0.0,
            temperature=0.0,
            stream=True,
            max_tokens=2000,
        )
        if response:
            for chunk in response:
                content = chunk.choices[0].delta.content
                self._PrintWithTypewriterEffect(content)
        return response

    @public
    def CreateKnowledgeBase(self, all_knowledge):
        self.embeddings.CreateKnowledgeBase(all_knowledge)

    @public
    def QueryKnowledgeBase(self, query_text, k=2, verbose = True):
        self.embeddings.QueryKnowledgeBase(query_text, k, verbose)

    @private
    def _PrintWithTypewriterEffect(self, text, delay=0.05):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
