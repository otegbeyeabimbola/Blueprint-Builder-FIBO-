# 🏗️ Blueprint Builder: The JSON-Native Compliance Engine

[![FIBO Hackathon](https://img.shields.io/badge/Submission-FIBO_Hackathon_2025-blueviolet?style=for-the-badge)](https://bria.ai)
[![Category](https://img.shields.io/badge/Category-Best_Agentic_Workflow-FFD700?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()

> **"Traditional AI generation breaks brand consistency. Blueprint Builder enforces it."**

**Blueprint Builder** is an intelligent, automated pipeline designed for the **Bria FIBO** model. It moves beyond simple text prompting by using a "Semantic Bridge" of custom ComfyUI nodes to validate, enforce, and self-correct visual parameters before a single pixel is generated.

Built by **Mohammed B. Kemal** & **Abimbola A. Otegbeye**.

---

## 🎥 Project Demo
[![Watch the Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID_HERE/maxresdefault.jpg)](YOUR_VIDEO_LINK_HERE)
*(Click to watch our <3 minute submission video)*

---

## 🚀 The Problem & Solution

### 🔴 The Problem: Ambiguity in Production
In professional workflows, a text prompt like *"make it warmer"* is dangerous. It might change the lighting, the skin tone, or the white balance unpredictably. Studios waste 40% of their time on visual QA because they lack deterministic control.

### 🟢 The Blueprint Solution: Agentic Compliance
We treat image generation as a **schema validation problem**.
1.  **Agents, not Prompts:** An intelligent agent converts a brief into a rigid JSON structure.
2.  **Pre-Flight Checks:** Our custom **Compliance Checker Node** validates the JSON against brand rules (e.g., "Must use Hex Code `#FF5733`" or "Must be `Sony A7R` sensor").
3.  **Self-Correction:** If a rule is violated, the agent **auto-corrects the JSON** instantly, ensuring 100% compliant outputs at scale.

---

## ⚙️ Technical Architecture: "The Semantic Bridge"

We developed a custom suite of ComfyUI nodes that act as the bridge between raw JSON logic and the FIBO generation model.

### 1. `JSON Input Agent Node` (The Translator)
Bypasses standard text encoders. It parses raw JSON into discrete, structured data types (`Camera_Params`, `Lighting_Params`) that feed directly into FIBO's disentangled layers.

### 2. `Compliance Checker Node` (The Enforcer)
* **Input:** Proposed JSON Blueprint + Brand Style Schema (Pydantic).
* **Logic:** Validates every parameter. If `aspect_ratio` is `1:1` but the brand requires `16:9`, it flags the error and outputs a **patched, compliant JSON**.
* **Result:** Zero "hallucinated" styles.

### 3. `JSON Output Reporter Node` (The Archivist)
Embeds the final, validated JSON blueprint into the generated image's EXIF/Metadata. This creates **Self-Documenting Assets**—drag the image back into ComfyUI to retrieve the exact blueprint used to create it.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.10+
* [ComfyUI](https://github.com/comfyanonymous/ComfyUI) installed locally.
* **Bria FIBO Model** downloaded from [Hugging Face](https://huggingface.co/briaai).

### Step 1: Clone the Repo
```bash
git clone [https://github.com/otegbeyeabimbola/Blueprint-Builder-FIBO-Json-Compliance-Engine](https://github.com/otegbeyeabimbola/Blueprint-Builder-FIBO-Json-Compliance-Engine)
cd blueprint-builder-fibo
````

### Step 2: Install Custom Nodes

Copy the `comfyui_custom_nodes` folder content into your ComfyUI installation:

```bash
cp -r src/custom_nodes/* path/to/ComfyUI/custom_nodes/
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Agent

1.  Launch ComfyUI.
2.  Load the workflow file: `workflows/blueprint_builder_demo.json`.
3.  Run `python src/agent_core.py` to generate your initial JSON blueprints.

-----

## 🏆 Award Category Alignment

**Submitted for: Best JSON-Native or Agentic Workflow**

  * **JSON-Native:** We don't just "support" JSON; we require it. Our entire pipeline relies on the structured nature of FIBO to perform diffs, merges, and validations that are impossible with text.
  * **Agentic:** The system reasons about the output. It knows *why* an image is wrong (e.g., "Lighting is Ambient, should be Studio") and fixes it autonomously.
  * **Production Ready:** Features like **Hex-Code Enforcement** and **Metadata Embedding** are specifically designed for enterprise adoption.

-----

## 👥 Contributors

  * **Mohammed B. Kemal** - [Email](mailto:mickymicky718@gmail.com)
  * **Abimbola A. Otegbeye** - [Email](mailto:otegbeyeabimbola2017@gmail.com)

-----

*Built with ❤️ for the Bria FIBO Hackathon 2025.*

```
```

## ⚖️ Copyright & License

Copyright © 2025 **Mohammed B. Kemal** and **Abimbola A. Otegbeye**. All Rights Reserved.

This project is submitted for the **FIBO Hackathon 2025**.
