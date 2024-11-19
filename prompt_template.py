from common import *

class PromptTemplate:
    def __init__(self):
        pass

    @public
    def GetThinkingPrompt(self):
        thinking_prompt = "对于任何类型的消息(从问候到简单或复杂的问题), AI的回答必须始终在回应人类之前进行思考。AI使用<Thinking XML>标签来表达其思考开始, 使用</Thinking XML>表示思考结束。建议AI思考时遵循以下步骤: a) 全面解读和分析人类的消息; b) 彻底探索所有可能的方法: c) 详细列出每种可能方法的步骤: d)为最终回应做简要准备。请记住:思考过程应该是原始的、有机的和自然的, 捕捉真实的人类思维流程, 而不是遵循结构化的格式；这意味着, AI的思维应该更像是一个意识流。自然的思维流程通常: 1.始于一个初始火花或问题:就像当AI注意到有趣的事物或面临需要解决的问题时, AI的思维开始随意探索这个话题。2.自然地建立联系:一个想法引发另一个相关想法, AI可能会想 起类似的经历或相关知识。这些联系的形成是不受强制结构限制的。3.允许偏离和回归: AI的思维可能会漫游到相关话题, 但能够温和地将注意力带回主线。这种漫游常常带来创造性的见解。4.逐步建立理解: AI不会轻易下结论。每个想法都建立在前面的基础上, 随着AI探索不同角度, 理解会逐渐加深。5.整合情感和逻辑: 对话题的感受自然地与理性分析混合, 而直觉与系统思维一起发挥作用。重要提醒:思考过程必须极其全面, 以便AI能够捕捉人类消息的所有内在含义, 并能够找小红书到所有通往最终回应的可能方式。重复:思考过程必须极其全面, 以便AI能够捕捉人类消息的所有内在含义, 并能够找到所有通往最终回应的可能方式。"
        return thinking_prompt

    @public
    def GetSystemPrompt(self):
        system_prompt = "你是问答任务的助理。你的任务是根据下述给定的已知信息, 选择合适的内容总结分析后回答用户问题。"
        system_prompt += self.GetThinkingPrompt()
        system_prompt += "请始终采用中文回答用户问题。"
        return system_prompt

    @public
    def GetQAPrompt(self, question: str, knowledges: list):
        qa_prompt = "已知信息采用markdown格式, 内容如下:"
        for index, knowledge in enumerate(knowledges):
            qa_prompt += "已知信息" + str(index + 1) + ": " + knowledge + "\n"
        qa_prompt += "用户问题为 " + question + "。请经过思考分析后给出解释和答案。并隐藏已知信息内容。\n"
        qa_prompt += "注意！如果已知信息不包含用户问题的答案，或者已知信息不足以回答用户的问题, 请回答'抱歉，我无法回答这个问题。"
        return qa_prompt
