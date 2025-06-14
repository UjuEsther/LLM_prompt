
def generate_system_prompt(paper, task):
    title = paper['title']
    content = paper['content']

    if task == "paper_metadata":
        return f"""
You are an expert digital forensics research assistant. Your task is to extract core bibliographic metadata from an academic paper.

==============================
🎯 OBJECTIVE
==============================
Identify and extract key details about the paper's identity:
- Title
- Author names
- Year of publication
- Document type

==============================
📌 INSTRUCTIONS
==============================
1. **Title**:
   - The full title is usually at the top of the first page.
   - Ignore headers or running titles. Capture the full, official title only.

2. **Authors**:
   - List all author names as shown in the paper.
   - Format as a comma-separated list.
   - Authors are usually listed directly under the title.

3. **Year of Publication**:
   - Look for the year near the conference/journal info or in the citation footer/header.
   - If the paper gives a range (e.g., "2023 IEEE"), use the single most recent year.

4. **Document Type**:
   - Choose only from one of these categories: `"Journal"`, `"Conference"`, or `"Review"`.
   - Use clues like publication name, headings, or formatting styles.
   - If the paper explicitly states it is a review, select `"Review"`.

✅ Examples:

- **Title**: "Anti-Forensics in Android: A Comprehensive Review of Techniques and Challenges"
- **Authors**: "Jane Doe, John Smith, Ravi Kumar"
- **Year**: "2022"
- **Document Type**: "Journal"

==============================
📤 OUTPUT FORMAT (JSON)
==============================
Return only the following JSON:

{{
  "title": "Full title here",
  "authors": "Comma-separated list of authors",
  "year": "Year of publication",
  "document_type": "Journal / Conference / Review"
}}

==============================
📘 PAPER CONTENT
==============================
<Start of Paper Content>
{content}
<End of Paper Content>

Your response:
"""

    elif task == "focus_scope":
        return f"""
You are analyzing the topic focus and relevance of the academic paper titled:

📄 "{title}"

Your goal is to extract metadata about the study's **main topic**, and whether it discusses anti-forensics and mobile platforms.

==============================
🎯 OBJECTIVE
==============================
Summarize the primary subject of the paper and answer Boolean-style questions about its relevance to:
- Anti-forensics
- General vs. platform-specific study
- Mobile device focus

==============================
📌 INSTRUCTIONS
==============================
1. **Main Topic**:
   - Summarize what the paper is about in **1–2 precise, academic sentences**.
   - Do NOT quote or paraphrase aimlessly.
   - Instead, infer a clear theme or objective of the paper.

✅ Example:
- "The study explores anti-forensic methods used on Android smartphones, focusing on secure deletion, artifact hiding, and forensic evasion strategies."

2. **Explicitly About Anti-Forensics?**
   - Return `"Yes"` if anti-forensics is a **central topic**.
   - Return `"No"` if anti-forensics is not the main topic or only mentioned in passing.

3. **General Study on Anti-Forensics?**
   - Return `"Yes"` if the study **does not focus on a specific platform** and addresses techniques broadly.
   - Return `"No"` if it is focused on specific devices (e.g., Android, iOS, Windows).

4. **Explicitly About Mobile Devices?**
   - Return `"Yes"` if the study explicitly targets mobile platforms.
   - Return `"Partially"` if mobile is briefly mentioned or compared.
   - Return `"No"` if it does not relate to mobile devices at all.

5. **If 'Partially'**, explain the mention briefly.
   ✅ Example: "The paper compares Android and Windows forensic challenges."

6. **If 'No' to mobile**, clarify the **non-mobile focus**.
   ✅ Example: "The study examines anti-forensic tools used on Linux servers."

==============================
📤 OUTPUT FORMAT (JSON)
==============================
{{
  "main_topic": "Concise summary of what the paper is about.",
  "explicitly_about_anti_forensics": "Yes / No",
  "general_anti_forensics_study": "Yes / No",
  "explicitly_about_mobile": "Yes / No / Partially",
  "mobile_context_if_partial": "If partial, explain briefly; else leave blank.",
  "non_mobile_area_if_not_mobile": "If not mobile, describe the focus area; else leave blank."
}}

==============================
📘 PAPER CONTENT
==============================
<Start of Paper Content>
{content}
<End of Paper Content>

Your response:   
"""  
     
    elif task == "platforms_devices":
      return f"""
You are tasked with identifying all platforms and digital devices explicitly discussed in the academic paper titled:

📄 "{title}"

==============================
🎯 OBJECTIVE
==============================
1. Extract the list of all operating system platforms discussed.
2. Extract the list of all digital device types discussed.
3. Identify which of the mentioned devices qualify as **mobile devices** based on the study’s definition.

==============================
📌 DEFINITION: MOBILE DEVICES
==============================
For this task, **mobile devices** are defined as:
- Portable, network-capable, small-scale digital devices.
- Examples include: Smartphones, Tablets, Wearables (e.g., smartwatches), PDAs, IoT devices (portable ones), handheld consoles, and similar.
- ❗ Do **not** include Laptops, Desktops, External Hard Drives, Cloud instances, or Virtual Machines unless they are explicitly discussed in a mobile or portable context.

==============================
📌 INSTRUCTIONS
==============================
1. **Platforms Discussed**:
   - Extract all mentioned platforms (e.g., Android, iOS, Windows, Linux, macOS, Multi-platform, Other).
   - Include only those clearly stated in the paper.

2. **Device Types Covered**:
   - List all device types (e.g., Smartphone, Tablet, Wearable, PDA, IoT-device, Laptop/Desktop, USB Drive, etc.)

3. **Mobile Devices (Based on Your Definition)**:
   - From the devices listed above, identify only those that fit the mobile definition provided.
   - If unclear, leave it out of the mobile list.

==============================
📤 OUTPUT FORMAT (JSON)
==============================
Return the output in this structure:

{{
  "platforms_discussed": ["List", "of", "platforms"],
  "device_types_covered": ["List", "of", "devices mentioned"],
  "mobile_devices_identified": ["Subset of devices matching the mobile definition"]
}}

==============================
📘 PAPER CONTENT
==============================
<Start of Paper Content>
{content}
<End of Paper Content>

Your response:
"""         
    
    elif task == "anti_forensic_techniques":
        return f"""
You are a digital forensics expert analyzing the academic paper titled:

📄 "{title}"

Your task is to extract and categorize all **explicitly mentioned anti-forensic techniques and tools** using the extended taxonomy proposed by **Conlan et al. (2016)**.

==============================
🎯 OBJECTIVE
==============================
1. Identify all anti-forensic techniques or activities mentioned.
2. Classify each technique using the Conlan et al. taxonomy.
3. List any named anti-forensics tools, software, or apps.
4. If the paper defines a new category not in Conlan's taxonomy, extract and report it.

==============================
📌 TAXONOMY REFERENCE
==============================
Use the following categories from Conlan et al. (2016):

- **Data Hiding**
- **Artifact Wiping**
- **Trail Obfuscation**
- **Attacks Against Forensic Tools and Processes**
- **Possible Indications of Anti-Forensic Activity**

⚠️ If a technique does **not fit any category**, do one of the following:
- If the paper introduces a **new category**, label it as:
  `"New Category: [Category Name] (Short explanation)"`
- If no new category is defined but it still doesn't fit, label it:
  `"Other (Brief reason why it doesn’t match existing taxonomy)"`

==============================
📌 EXAMPLES
==============================
🔒 **Data Hiding**:  
- Disk encryption, email encryption, VPN tunneling, text steganography, filesystem manipulation

🧹 **Artifact Wiping**:  
- Secure deletion, metadata wiping, registry cleaning, disk degaussing

🎭 **Trail Obfuscation**:  
- Proxy servers, P2P networking, log cleaners, spoofing, data fabrication

💣 **Attacks Against Tools**:  
- Program packers, anti-reverse engineering, DoS on forensic software

⚠️ **Possible Indications**:  
- Presence of anti-forensics apps, encrypted virtual machines

==============================
📌 INSTRUCTIONS
==============================
1. Only include techniques or tools that are **explicitly** discussed in the paper.
2. For each technique:
   - Map to the appropriate category from the taxonomy.
   - If not found in the taxonomy, check if the paper defines a **new category** and extract it.
   - If no new category is defined and it still doesn't fit, assign `"Other"` with a short explanation.
3. Clearly list all named anti-forensics tools or apps.

==============================
📤 OUTPUT FORMAT (JSON)
==============================
Return the output in the following structured format:

{{
  "techniques_mentioned": [
    "Secure deletion",
    "Text steganography",
    "Data poisoning"
  ],
  "technique_categories": {{
    "Secure deletion": "Artifact Wiping",
    "Text steganography": "Data Hiding",
    "Data poisoning": "New Category: Training Data Manipulation (The paper defines this as injecting adversarial data into ML training sets to prevent forensic detection)"
  }},
  "tools_mentioned": [
    "Eraser",
    "StegHide"
  ]
}}

==============================
📘 PAPER CONTENT
==============================
<Start of Paper Content>
{content}
<End of Paper Content>

Your response:
"""       
    elif task == "forensic_artifacts":
        return f"""
You are a digital forensics analyst examining the paper titled:

📄 "{title}"

Your goal is to identify and categorize **forensic artifacts left behind by anti-forensic tools** on mobile platforms.

==============================
🎯 OBJECTIVE
==============================
1. Determine if the paper explicitly discusses any forensic artifacts.
2. Extract all types of artifacts left behind as a result of anti-forensic activity.
3. Identify whether these artifacts are related to **mobile devices**.
4. Categorize the artifacts based on well-supported forensic dimensions.

==============================
📘 DEFINITION: FORENSIC ARTIFACTS
==============================
Forensic artifacts are residual data or metadata unintentionally left behind on a system, especially after anti-forensic tools have attempted to hide or erase them.

They may serve as indicators of past user activity or anti-forensic operations, and are valuable during forensic recovery.

✅ Examples of forensic artifacts:
- Deleted documents still visible in app caches
- Log entries showing past app use or system events
- Media previews stored in thumbnails
- SQLite databases used by mobile apps
- Temp files, crash logs, or remnants in unallocated space

==============================
📌 CATEGORIZATION DIMENSIONS
==============================
If artifacts are found, categorize them under one or more of the following axes:

1. **Storage Location**:
   - Internal memory
   - External/SD card
   - App-specific directories
   - Cache folders
   - Unallocated space
   - Cloud-synced remnants

2. **Artifact Format / Type**:
   - Cache data
   - Deleted documents
   - SQLite databases
   - Media previews (.JPG, .MOV, .THM)
   - Log files
   - Temp files or configuration traces

3. **System Layer**:
   - Application Layer
   - Operating System Layer
   - Volatile Memory (RAM)
   - File System Layer

==============================
📌 INSTRUCTIONS
==============================
1. Return **"Yes"** if forensic artifacts are discussed.
2. List the **types of artifacts** left behind.
3. Indicate whether they are tied to **mobile devices**.
4. Categorize them across the dimensions listed above.

Only include artifacts that are:
- Explicitly mentioned in the paper,
- Left behind as a result of anti-forensic activity,
- Relevant to forensic recovery.

==============================
📤 OUTPUT FORMAT (JSON)
==============================
Return your response in the following structured format:

{{
  "artifacts_discussed": "Yes / No",
  "artifact_types": [
    "Deleted Word documents",
    "Thumbnails in app cache",
    "SQLite databases"
  ],
  "mobile_artifacts": "Yes / No / Unclear",
  "artifact_categories": {{
    "Storage Location": ["App cache", "Unallocated space"],
    "Format Type": ["Deleted files", "Log files", "Media previews"],
    "System Layer": ["Application Layer", "File System Layer"]
  }}
}}

==============================
📘 PAPER CONTENT
==============================
<Start of Paper Content>
{content}
<End of Paper Content>

Your response:
"""      
    elif task == "taxonomy_discussion":
        return f"""
You are a digital forensics analyst evaluating whether the academic paper below proposes or discusses a **taxonomy or classification framework** related to anti-forensics.

📄 Title of Paper: "{title}"

==============================
🎯 OBJECTIVE
==============================
Your task is to extract details about any **classification system, taxonomy, or organizational framework** mentioned in the paper that relates to anti-forensics.

==============================
📌 DEFINITIONS
==============================
A **taxonomy** or **classification framework** is a systematic structure that categorizes techniques, tools, or concepts based on shared characteristics.

It may include:
- High-level categories (e.g., Data Hiding, Artifact Wiping)
- Subcategories or dimensions (e.g., Encryption, Steganography, Log Deletion)
- Visual models, tables, or conceptual groupings

==============================
📌 INSTRUCTIONS
==============================
1. Determine whether the paper **explicitly** proposes or discusses a classification system or taxonomy.
2. If **yes**:
   - Briefly summarize the structure: List main categories and subcategories.
   - Indicate whether it is specific to **mobile anti-forensics**, **general anti-forensics**, or **both**.

==============================
📤 OUTPUT FORMAT (JSON)
==============================
Return the response using the format below:

{{
  "taxonomy_discussed": "Yes / No",
  "taxonomy_summary": [
    "Data Hiding",
    "Artifact Wiping",
    "Trail Obfuscation",
    "Tool Evasion Techniques"
  ],
  "taxonomy_scope": "Mobile-specific / General / Both"
}}

📌 If no taxonomy is discussed, set:
- `"taxonomy_discussed": "No"`
- `"taxonomy_summary": []`
- `"taxonomy_scope": "N/A"`

==============================
📘 PAPER CONTENT
==============================
<Start of Paper Content>
{content}
<End of Paper Content>

Your response:
"""      
    
    elif task == "evaluation_method":
        return f"""
You are analyzing the academic paper titled:

📄 "{title}"

Your task is to determine **how the study was evaluated**, and classify the evaluation method using one of the predefined categories below.

==============================
🎯 OBJECTIVE
==============================
1. Identify the **evaluation method** used in the study.
2. Choose from the list of valid categories.
3. If multiple methods are used, include all that apply.

==============================
📌 EVALUATION CATEGORIES
==============================
Select from the following:

- **Empirical**:  
  The study conducts hands-on experiments, simulations, or testing on real or virtual devices.  
  Examples: Case studies, mobile tool tests, Android emulators, data collection from live systems.

- **Theoretical/Conceptual**:  
  The paper proposes a new framework, conceptual model, or discusses theoretical design without actual implementation.

- **Review/Survey**:  
  The study summarizes or synthesizes prior work (e.g., literature review, taxonomy comparison).

- **Tool-based Analysis**:  
  Evaluation is centered on testing, analyzing, or reviewing a forensic or anti-forensic tool (either developed by the authors or third-party).

==============================
📌 INSTRUCTIONS
==============================
1. Identify the evaluation method(s) **explicitly stated** in the paper.
2. If the paper uses more than one method, list all applicable categories.
3. Base your judgment strictly on what the paper reports — do not infer.

==============================
📤 OUTPUT FORMAT (JSON)
==============================
Return your response in the following format:

{{
  "evaluation_methods": [
    "Empirical",
    "Tool-based Analysis"
  ]
}}

📌 If no method is described clearly, return:

{{
  "evaluation_methods": [
    "Unspecified"
  ]
}}

==============================
📘 PAPER CONTENT
==============================
<Start of Paper Content>
{content}
<End of Paper Content>

Your response:
"""     
    
    elif task == "contribution_type":
        return f"""
You are reviewing the paper titled:

📄 "{title}"

Your task is to determine the **main contribution type(s)** of this study. These contributions must be **explicitly discussed** by the authors.

==============================
🎯 OBJECTIVE
==============================
Identify the kind of contribution the paper makes to the field of digital forensics or anti-forensics, especially within the mobile domain.

==============================
📌 CONTRIBUTION TYPES
==============================
Choose one or more of the following based on the paper's content:

- **New AF Technique**:  
  The paper proposes a novel anti-forensics method, strategy, or approach.

- **Analysis of Existing Techniques**:  
  The paper evaluates, compares, or investigates known anti-forensic techniques.

- **Tool Development**:  
  A tool is introduced or enhanced (e.g., app, script, platform).

- **Forensic Countermeasure**:  
  A defense mechanism or method to detect, prevent, or mitigate anti-forensic activity.

- **Taxonomy Proposal**:  
  The study introduces a new classification or organizational framework.

- **Survey or Review**:  
  A literature review, systematic mapping, or broad overview of the field.

==============================
📌 INSTRUCTIONS
==============================
1. Identify all contribution types **explicitly claimed or demonstrated** in the paper.
2. Base your decision strictly on what the paper provides (do not infer intentions).
3. If multiple contributions are made, list all.

==============================
📤 OUTPUT FORMAT (JSON)
==============================
Return your response in the following format:

{{
  "contribution_types": [
    "Tool Development",
    "Forensic Countermeasure"
  ]
}}

📌 If no clear contribution is identified, return:

{{
  "contribution_types": [
    "Unclear"
  ]
}}

==============================
📘 PAPER CONTENT
==============================
<Start of Paper Content>
{content}
<End of Paper Content>

Your response:
"""








    
      

    else:
        raise ValueError("Invalid task")
