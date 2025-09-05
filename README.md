# 🧠 SmartCLI: An Agentic AI-Powered Bash Companion

## Overview

**SmartCLI** is a next-generation, multi-modal command-line interface engineered to elevate the Bash experience across the skill spectrum. Designed to remain invisible to power users while guiding beginners with contextual intelligence, SmartCLI redefines shell interaction through semantic command suggestions, conversational assistance, and autonomous error resolution.

At its core, SmartCLI is an **agentic AI system**—capable of reasoning, adapting, and conversing—built to foster intuitive learning and accelerate command-line mastery. It also integrates **Retrieval-Augmented Generation (RAG)** to deliver hyper-personalized answers grounded in user-provided files and directories.

---

## Key Features

### Context-Aware Command Recommendations
- Real-time suggestions based on shell state and user intent.
- AI-powered autocompletion with semantic understanding.
- Learns from usage patterns to improve relevance over time.

### Beginner Learning Mode
- Dedicated instructional interface for CLI newcomers.
- Stepwise command breakdowns with inline explanations.
- Interactive scaffolding that builds confidence and fluency.

### Multi-Modal Conversational Agent
- Accepts natural language queries beyond Bash syntax.
- Capable of answering technical questions, offering insights, or engaging in casual dialogue.
- Seamlessly transitions between instructional and conversational tones.

### Autonomous Error Debugging
- Detects and diagnoses runtime errors in Bash scripts.
- Suggests corrective actions or auto-applies fixes with user approval.
- Tracks error patterns to improve future resilience.

### Retrieval-Augmented Personalization (RAG)
- Automatically activates when general questions are asked.
- Retrieves relevant content from user-specified files and folders.
- Grounds responses in local context—ideal for project-specific queries, config analysis, or environment-aware suggestions.

### Non-Intrusive Design Philosophy
- Operates in parallel with native Bash workflows.
- Advanced users experience zero friction or interruption.
- Suggestions and guidance are opt-in, never enforced.


## 🧪 Usage Modes

### 1. **Standard Mode**
- Minimalist overlay for command suggestions.
- Ideal for power users seeking occasional assistance.

### 2. **Learning Mode**
- Rich instructional interface with guided walkthroughs.
- Includes sandboxed command simulations and feedback loops.

### 3. **Debug Mode**
- Activated upon error detection.
- Offers fix suggestions, root cause analysis, and optional auto-repair.

---

## 🚀 Getting Started

If you don't have uv installed, you can install it using the following command:

```bash
git clone https://github.com/arpangautam/nexcli.git
```

Paste your openrouter api key in the .env file

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

```bash
cd smartcli
```

```bash
uv pip install
```

```bash
uv run nexcli
```

To personalize with local context enable RAG:

config.json
```bash
{
    "RAG": true,
    "folder": "PATH_TO_YOUR_CONTEXTS"
}   
```

SmartCLI will automatically use RAG to tailor its response based on your project files.

---

## 🧠 Philosophy

SmartCLI embodies a **pedagogically aware, agentic AI ethos**—not merely automating tasks, but cultivating understanding. It respects the autonomy of advanced users while nurturing the growth of beginners, all within a frictionless shell-native environment. With RAG capabilities, it becomes not just a CLI assistant, but a deeply contextualized co-pilot for your unique development environment.