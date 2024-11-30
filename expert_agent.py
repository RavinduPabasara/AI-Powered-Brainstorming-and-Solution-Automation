# expert_agent.py
from ai_assistant_factory import AIAssistantFactory

class ExpertAgent:
    def generate_contribution(client, conversation_history, speaker, expertise, question=None, target=None):
        try:
            formatted_history = "\n".join([f"{msg['speaker']}: {msg['content']}" for msg in conversation_history])

            if question:
                prompt = (f"You are {speaker}, an expert in {expertise}. "
                          f"You've been asked: '{question}' by {target}. "
                          f"Provide a concise, insightful answer based on your expertise and the ongoing discussion. "
                          f"Your response should build upon previous contributions and avoid repeating information. "
                          f"Always answer in a paragraph. Keep your response between 50-80 words.\n\n"
                          f"Discussion so far:\n{formatted_history}\n\n"
                          f"Your response as {speaker}:")
            else:
                prompt = (f"You are {speaker}, an expert in {expertise}. "
                          f"You're continuing the brainstorming on: '{conversation_history[0]['content'].split(': ')[1]}'. "
                          f"Contribute an insight from your expertise, building upon previous contributions and "
                          f"avoiding repetition. Reference others if relevant and move the discussion forward. "
                          f"Always answer in a paragraph. Keep your response between 80-120 words.\n\n"
                          f"Discussion so far:\n{formatted_history}\n\n"
                          f"Your contribution as {speaker}:")

            response = AIAssistantFactory.api_call_with_delay(client, prompt)
            return response.strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"{speaker} encountered an error and couldn't contribute."

    def generate_question(client, conversation_history, speaker, expertise, target):
        try:
            formatted_history = "\n".join([f"{msg['speaker']}: {msg['content']}" for msg in conversation_history])
            prompt = (f"You are {speaker}, an expert in {expertise}. "
                      f"Based on the ongoing discussion, formulate a targeted question for {target} "
                      f"that relates to their expertise and moves the conversation forward. "
                      f"Your question should build upon previous contributions and explore new aspects "
                      f"of the topic that haven't been addressed yet. "
                      f"Keep your question concise and specific.\n\n"
                      f"Discussion so far:\n{formatted_history}\n\n"
                      f"Your question for {target}:")

            response = AIAssistantFactory.api_call_with_delay(client, prompt)
            return response.strip()
        except Exception as e:
            print(f"Error generating question: {e}")
            return f"{speaker} encountered an error and couldn't ask a question."