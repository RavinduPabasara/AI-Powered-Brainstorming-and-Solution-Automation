#brainstorming_manager.py
from ai_assistant_factory import AIAssistantFactory

class BrainstormingManager:
    def check_progress(client, conversation_history, goal):
        try:
            formatted_history = "\n".join([f"{msg['speaker']}: {msg['content']}" for msg in conversation_history])
            prompt = (f"As a neutral observer, assess the progress of the following brainstorming session "
                    f"towards the goal: '{goal}'. Provide a brief summary of key points discussed "
                    f"and suggest areas that need further exploration. Keep your response under 100 words.\n\n"
                    f"Discussion so far:\n{formatted_history}\n\n"
                    f"Progress assessment:")

            response = AIAssistantFactory.api_call_with_delay(client, prompt)
            return response.strip()
        except Exception as e:
            print(f"Error checking progress: {e}")
            return "Unable to assess progress due to an error."