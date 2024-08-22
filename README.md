# gensec-Liu-yuxuan

This repository includes all of the projects that I have conducted during the 2024 summer internship. Below is the description for my final project "Automating Protection against Prompt Injections for Large Language Models".

## Autoguard
**An automating protection application that secures a user's LLM application from prompt injections**

### A brief overview of its design
Autoguard receives a developer's LLM application as input and inserts it into a pre-written prompt template to create a prompt or instructions on implementing a security system onto the original application in the form of a LangGraph. This prompt is sent to ChatGPT to generate the securd LLM application.

![Our approach for designing the Autoguard](/agent_security/visuals/our_approach.png)

LangGraphs are frameworks that allow multi-actor collaboration by connecting and splitting tasks among multiple LLM agents. Their graphical and flow-chart style helps developers visualize their programs, improving efficiency and understanding of LLM structures.

In the following LangGraph example provided by **LangChain**, data follows the arrows from one node to the next, with each node serving a distinct purpose such as text generation and determination of text completeness.

Please find the image source in LangChain's website: https://www.langchain.com/langgraph


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

For convenience sake, you can install all of the necessary imports using the following command line.

```
python3 install -r requirements.txt
```

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/Yu1623/gensec-liu-yuxuan.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/Yu1623/gensec-liu-yuxuan/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
