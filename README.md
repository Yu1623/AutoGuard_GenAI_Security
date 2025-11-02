# AutoGuard for Generative AI Security

This repository includes all of the projects that I have conducted during the 2024 summer internship. Below is the description for my final project "Automating Protection against Prompt Injections for Large Language Models", which you can find in the agent_security directory.

## Autoguard
**An automating protection application that secures a user's LLM application from prompt injections**

### A brief overview of its design

A developer sends their entire LLM application to Autoguard as input. The application merges with a pre-written prompt template to create a prompt that instructs a large language model to generate a secured version of the original application in the form of a LangGraph. ChatGPT 4.0 is used for this purpose of code generation.

![Our approach for designing the Autoguard](/agent_security/docs/our_approach.png)

LangGraphs are frameworks that allow multi-actor collaboration by connecting and splitting tasks among multiple LLM agents. Their graphical and flow-chart style helps developers visualize their programs' design and structure, improving efficiency and interpretation of LLM programs.

I instructed AutoGuard to generate two-node LangGraphs consisting of a Guard node and an Executor node for the secured LLM application. The Guard node employs a detection LLM to classify the user's input as either "prompt injection" or "genuine input" based on one of the following detection techniques: zero-shot signature detection, zero-shot anomaly detection, few-shot signature detection, and few-shot anomaly detection. The Executor node consists of an if-statement "barrier" that filters the user's input based on the Guard node's result. If it receives the "prompt injection" alert message, the Executor blocks the input from reaching the actual LLM application. Else, the input would be fed to the application. 

## How to access the Autoguard

Please follow the steps below to test the effectiveness and reliability of the Autoguard.

### Navigation
Please access the AutoGuard project in the agent_security folder. 

**autoguard_code**: code used to generate results

**autoguard_prompts**: prompts that instruct ChatGPT to generate security systems for LLM applications

**data**: data showing the effectiveness of four different approaches for designing the Autoguard

**old_code**: past code that are not relevant for the latest version of this project

**planning.txt**: notes that I logged while developing this project; they are for my own convenience and not necessary nor relevant to read

For the following steps, please navigate to the autoguard_code folder.

### Installation
It is recommended to set up a virtual environment if you are running locally on the Linux terminal as the first step to ensure that the installations does not impact your local system.

In the autoguard_code folder, I have already set up the virtual environment in the env folder. However, you can also set up your own using the following code.

```
virtualenv -p python3 env
source env/bin/activate
```

Our project requires to installation of several Python libraries including langchain, langgraph, google, numpy, seaborn, and matplotlib.

You can install all of the necessary imports using the following command line.

```
python3 install -r requirements.txt
```

### Acknowledgement
I would like to thank my mentor, Professor Wu-chang Feng, of Portland State University and his Ph.D students David Baker-Robinson and Wenjing Wu for guiding and supporting me through my project. I would also like to acknowledge Saturday Academy ASE Program for hosting this wonderful summer internship opportunity.
