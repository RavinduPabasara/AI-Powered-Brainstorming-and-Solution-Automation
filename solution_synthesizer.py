#solution synthesizer.py
from ai_assistant_factory import AIAssistantFactory

class SolutionSynthesizer:
    def synthesize_solution(client, conversation_history, goal):
        try:
            formatted_history = "\n".join([f"{msg['speaker']}: {msg['content']}" for msg in conversation_history])
            prompt = (f"As a solution synthesizer, review the entire brainstorming session and propose a comprehensive "
                      f"solution that aligns with the goal: '{goal}'. Consider all expert contributions and integrate "
                      f"the best ideas. Provide a clear, actionable solution in 150-200 words.\n\n"
                      f"Full discussion:\n{formatted_history}\n\n"
                      f"Synthesized solution:")

            response = AIAssistantFactory.api_call_with_delay(client, prompt)
            return response.strip()
        except Exception as e:
            print(f"Error synthesizing solution: {e}")
            return "Unable to synthesize a solution due to an error."

    def design_implementation(client, synthesized_solution, goal):
        try:
            prompt = (
                f"As an expert software architect, design a high-level implementation plan for the following solution: "
                f"'{synthesized_solution}'\n"
                f"The goal is: '{goal}'\n"
                f"Propose a suitable tech stack, outline the main components of the system, and provide a brief "
                f"explanation of how they will work together. Include any necessary experts or specialized knowledge "
                f"required for implementation. Break down the implementation into at least 3-5 distinct parts. "
                f"Keep your response between 200-250 words.\n\n"
                f"Implementation design:")

            response = AIAssistantFactory.api_call_with_delay(client, prompt)
            return response.strip()
        except Exception as e:
            print(f"Error designing implementation: {e}")
            return "Unable to design implementation due to an error."
