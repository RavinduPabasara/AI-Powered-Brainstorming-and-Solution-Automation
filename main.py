#main.py
import os
import time
import random
import json
import re
from datetime import datetime
from openai import OpenAI
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from concurrent.futures import ThreadPoolExecutor, as_completed
from ai_assistant_factory import AIAssistantFactory
from nlp_processor import NLPProcessor
from expert_agent import ExpertAgent
from brainstorming_manager import BrainstormingManager
from solution_synthesizer import SolutionSynthesizer
from implementation_manager import ImplementationManager
from file_system_handler import FileSystemHandler

def main():
    create_llm=AIAssistantFactory.create_llm
    generate_question=ExpertAgent.generate_question
    generate_contribution=ExpertAgent.generate_contribution
    check_progress=BrainstormingManager.check_progress
    synthesize_solution=SolutionSynthesizer.synthesize_solution
    design_implementation=SolutionSynthesizer.design_implementation
    extract_tech_stack=ImplementationManager.extract_tech_stack
    extract_implementation_parts= ImplementationManager.extract_implementation_parts
    implement_solution_part= ImplementationManager.implement_solution_part
    generate_readme=ImplementationManager.generate_readme
    save_implementation=FileSystemHandler.save_implementation

    try:
        num_experts = int(input("Enter the number of experts in the brainstorming session: "))
        topic = input("Enter the question for the experts to brainstorm: ")
        goal = input("Enter the goal of this brainstorming session: ")

        client = create_llm("gpt-4o-mini")
        experts = []

        for i in range(num_experts):
            expertise = input(f"Enter expertise for Expert {i + 1}: ")
            experts.append({"name": f"Expert {i + 1}", "expertise": expertise})

        conversation_history = [{'speaker': 'Moderator', 'content': f"Today's brainstorming question: {topic}"}]
        brainstorming_log = [{'topic': topic, 'goal': goal, 'experts': experts, 'rounds': []}]

        print(f"\nBrainstorming Question: {topic}")
        print(f"Goal: {goal}")
        for expert in experts:
            print(f"{expert['name']} Expertise: {expert['expertise']}")

        num_rounds = 3

        for i in range(num_rounds):
            print(f"\nRound {i + 1}:")
            round_contributions = {}

            for expert in experts:
                if random.choice([True, False]) and len(conversation_history) > 1:
                    target = random.choice([exp for exp in experts if exp != expert])
                    question = generate_question(client, conversation_history, expert["name"], expert["expertise"],
                                                 target["name"])
                    print(f"{expert['name']} asks {target['name']}:", question)

                    answer = generate_contribution(client, conversation_history, target["name"],
                                                   target["expertise"], question=question, target=expert["name"])
                    print(f"{target['name']} answers:", answer)

                    conversation_history.append({'speaker': expert["name"], 'content': question})
                    conversation_history.append({'speaker': target["name"], 'content': answer})
                    round_contributions[expert['name']] = question
                    round_contributions[target['name']] = answer
                else:
                    contribution = generate_contribution(client, conversation_history, expert["name"], expert["expertise"])
                    print(f"{expert['name']}:", contribution)
                    conversation_history.append({'speaker': expert["name"], 'content': contribution})
                    round_contributions[expert['name']] = contribution

            progress_assessment = check_progress(client, conversation_history, goal)
            print("\nProgress Assessment:", progress_assessment)
            conversation_history.append({'speaker': 'Progress Checker', 'content': progress_assessment})
            round_contributions['Progress Assessment'] = progress_assessment

            brainstorming_log[0]['rounds'].append({'round': i + 1, **round_contributions})

        print("\nBrainstorming session concluded.")

        # Synthesize solution
        synthesized_solution = synthesize_solution(client, conversation_history, goal)
        print("\nSynthesized Solution:")
        print(synthesized_solution)
        conversation_history.append({'speaker': 'Solution Synthesizer', 'content': synthesized_solution})
        brainstorming_log[0]['synthesized_solution'] = synthesized_solution

        # Design implementation
        implementation_design = design_implementation(client, synthesized_solution, goal)
        print("\nImplementation Design:")
        print(implementation_design)
        conversation_history.append({'speaker': 'Software Architect', 'content': implementation_design})
        brainstorming_log[0]['implementation_design'] = implementation_design

        # Extract tech stack and implementation parts using NLP techniques
        tech_stack = extract_tech_stack(implementation_design)
        implementation_parts = extract_implementation_parts(implementation_design)

        print(f"\nExtracted Tech Stack: {tech_stack}")
        print("Extracted Implementation Parts:")
        for part in implementation_parts:
            print(f"- {part}")

        # Implement solution using multiple threads
        print("\nImplementing the solution...")
        implemented_files = []

        with ThreadPoolExecutor(max_workers=len(implementation_parts)) as executor:
            future_to_part = {
                executor.submit(implement_solution_part, client, implementation_design, part,
                                tech_stack): part for part in implementation_parts}
            for future in as_completed(future_to_part):
                part = future_to_part[future]
                try:
                    result = future.result()
                    if result:
                        implemented_files.extend(result)
                        print(f"Implemented part: {part[:50]}...")
                        for file_name, _ in result:
                            print(f"  - Created file: {file_name}")
                    else:
                        print(f"Failed to implement part: {part[:50]}... (No files generated)")
                except Exception as e:
                    print(f"Failed to implement part: {part[:50]}... Error: {str(e)}")

        readme_content = generate_readme(client, topic, goal, synthesized_solution, implementation_design, tech_stack,
                                         [file[0] for file in implemented_files])
        implemented_files.append(("README.md", readme_content))

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if implemented_files:
            save_implementation(implemented_files, f"solution_{timestamp}")
            brainstorming_log[0]['implemented_files'] = [file[0] for file in implemented_files]
            print(f"\nImplementation completed. Total files created: {len(implemented_files)}")
        else:
            print("\nFailed to implement the solution. No files were generated.")

        # Save the updated brainstorming log
        filename = f"brainstorming_log_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(brainstorming_log, f, indent=2)
        print(f"Updated brainstorming log saved to {filename}")

    except ValueError as ve:
        print(f"A value error occurred: {ve}")
    except IOError as ioe:
        print(f"I/O error occurred: {ioe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()