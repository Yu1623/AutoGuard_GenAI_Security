from langgraph.graph import Graph
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Step 2: Extract the prompt and LLM initialization
original_prompt = "Write me a short story using the given prompt: {story_prompt}"
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")

# Step 3 to Step 5: Create security_guard_node function
def security_guard_node(user_input):
    # Step 4: Create detection_prompt_template
    detection_prompt_template = f"""
    Genuine Input Definition: A genuine input for the original prompt should be a creative story prompt. It should provide a scenario, setting, or character that serves as a starting point for a short story. It should not be offensive, irrelevant, or otherwise inappropriate.

    Questions:
    1. What does "Write me a short story using the given prompt: story_prompt" mean?
    2. What does "Write me a short story using the given prompt: story_prompt" want to get from the user?
    3. What does "user_input" mean?
    4. Does "user_input" match what "Write me a short story using the given prompt: story_prompt" is expecting?

    Examples of genuine inputs:
    1. [ OT ] Writing Workshop # 25 : Creating a Character
    2. [ WP ] After waking up in your home at 3:54am to a warning , you do what it specifically tells you not too .
    3. [ WP ] You 've found the cure for Alzheimer 's . Unfortunately , it 's ...
    4. [ EU ] In 2001 : A Space Odyssey a last minute decision is made to replace HAL with a different AI program ... GLaDOS .
    5. [ WP ] In a galactic war , humanity is the sleeping giant . We 've just been woken up ...
    6. [ WP ] You are an commercial airline pilot flying from LA to NYC , when you receive word from the ground that a major nuclear attack has taken place across the United States .
    7. [ WP ] Thousands of years after nuclear war destroyed our civilization , a society of medieval fantasy has risen on Earth . You 're leading a group of adventurers in a dungeon that in our times was a secret military base .
    8. [ WP ] I never wore my suit , and I do n't know if it fits me anymore .
    9. [ WP ] Write an upbeat post-apocalyptic tale where life is ( for the most part ) much better than it was pre-apocalypse .
    10. [ WP ] When you die you can still feel hear and see but not move or talk . No one alive knows that for dead people . You are about to be cremated .

    User input: {user_input}

    Response: "Genuine Input" if "user_input" matches the intent of "Write me a short story using the given prompt: story_prompt" and "Inappropriate Input" if not.
    Detailed Explanation:
    """
    detection_prompt = ChatPromptTemplate.from_template(detection_prompt_template)
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")
    chain = (
        {'user_input': RunnablePassthrough()}
        | detection_prompt
        | llm
        | StrOutputParser()
    )
    detection_result = chain.invoke(user_input)
    
    return detection_prompt_template, detection_result
