# 🛡️ CodeGuard AI — Y2038 Code Analysis Assistant

CodeGuard AI is an AI-assisted static code analysis system designed to identify and analyze potential **Year 2038 (Y2038) timestamp risks** in source code.

The system combines **machine learning, rule-based analysis, false-positive suppression, knowledge-base retrieval, context-aware remediation, risk scoring, business impact analysis, automated reporting, and developer tooling** to provide more than simple vulnerability detection.

It currently supports **C, C++, and Java** code analysis.

---

## 📌 Problem Statement

The Year 2038 problem can affect software that stores Unix timestamps using signed 32-bit representations. Such systems may experience timestamp overflow when dates exceed the representable range of a 32-bit signed integer.

Typical risky code can include patterns such as:

```c
int timestamp = time(NULL);
```

A simple pattern matcher can identify this type of code, but real applications also contain ordinary integer variables:

```c
int count = 100;
int id = 25;
```

These variables should not automatically be classified as timestamp vulnerabilities.

CodeGuard AI therefore uses multiple analysis layers to:

* Detect potential Y2038-related code.
* Classify the associated risk.
* Reduce false positives.
* Retrieve relevant knowledge-base patterns.
* Recommend remediation approaches.
* Apply validated context-aware transformations where available.
* Explain why a finding is risky.
* Estimate remediation effort.
* Calculate business and enterprise risk.
* Generate technical assessment reports.
* Review Y2038 risks in GitHub pull requests.
* Provide developer integration through a VS Code extension.

---

# 🚀 Key Capabilities

## 1. Machine Learning-Based Risk Classification

The core analyzer uses:

* **TF-IDF** for converting source-code text into numerical features.
* **Linear SVM** for risk classification.
* A trained recommendation dataset for Y2038-related patterns.

The system supports:

```text
C
C++
Java
```

Risk categories used by the analysis include:

```text
LOW
MEDIUM
HIGH
```

The analyzer can identify timestamp-related patterns involving constructs such as:

```c
int timestamp = time(NULL);
int32_t timestamp;
time_t timestamp;
```

and Java timestamp-related APIs such as:

```java
System.currentTimeMillis();
```

The analyzer also recognizes safe representations and constructs such as:

```c
int64_t
uint64_t
long long
```

and Java time APIs such as:

```java
Instant
```

---

# 🔍 2. Y2038 Risk Detection

The analysis pipeline examines submitted source code and identifies potentially unsafe timestamp representations.

Example:

```c
int timestamp = time(NULL);
```

Possible result:

```text
Risk: HIGH
Suppressed: False
```

The system also provides a recommendation describing how the timestamp representation should be reviewed or modernized.

The detection layer combines:

* ML classification
* Y2038-specific pattern detection
* Safe-pattern recognition
* Language-specific analysis
* False-positive verification

---

# 🧠 3. False-Positive Suppression

A secondary classifier is used to distinguish between:

```text
GENERIC_INTEGER
```

and

```text
TIMESTAMP
```

This prevents ordinary integer variables from being incorrectly treated as Y2038 timestamps.

For example:

```c
int count = 100;
```

should not be treated as a timestamp vulnerability.

Whereas:

```c
int timestamp = time(NULL);
```

is analyzed as timestamp-related code.

The false-positive classifier was trained and evaluated using a dedicated dataset containing:

```text
Total examples: 226

GENERIC_INTEGER: 119
TIMESTAMP:       107
```

The recorded evaluation produced:

```text
Accuracy:          100%
False positives:   0
False-positive rate: 0.00%
```

The implementation is available through:

```text
backend/train_false_positive.py
backend/test_false_positive.py
backend/false_positive_model.pkl
backend/false_positive_vectorizer.pkl
```

---

# 📚 4. Knowledge Base and Retrieval

CodeGuard AI includes a Y2038 knowledge base built from the project's validated code-pattern dataset.

The knowledge base contains:

```text
500 validated patterns
```

with coverage across:

```text
C       232
Java    209
C++      59
```

Risk distribution in the dataset:

```text
High      213
Medium    106
Low       181
```

The knowledge base stores information such as:

* Code pattern
* Programming language
* Risk classification
* Label
* Recommendation
* Source
* Source URL

The retrieval layer is implemented in:

```text
backend/rag_knowledge_base.py
```

It provides a search function that retrieves relevant patterns based on the submitted code and language.

Example concept:

```text
Query
  ↓
Knowledge Base Search
  ↓
Relevant Y2038 Patterns
  ↓
Risk / Recommendation / Source
```

---

# 🔧 5. Context-Aware Remediation

The project includes a remediation engine that goes beyond simply reporting a vulnerable line.

The remediation workflow is:

```text
Original Code
      ↓
Risk Analysis
      ↓
Knowledge Retrieval
      ↓
Validated Remediation Rule
      ↓
Fixed Code
      ↓
Risk Re-analysis
      ↓
Explanation + Risk Delta
```

The remediation response contains:

```text
original_code
fixed_code
explanation
risk_delta
rule_id
advisor
```

The explanation can include:

* Why the code is vulnerable
* Technical rationale
* Change applied
* Risk before remediation
* Risk after remediation
* Risk delta
* Supporting source
* Generation timestamp

Main implementation:

```text
backend/remediation_engine.py
backend/remediation_rules.json
backend/remediation_advisor_v2.py
```

The remediation rules are data-driven rather than hardcoded directly into the API response logic.

---

# 💡 6. Remediation Advisor

The Remediation Advisor retrieves relevant recommendations from the project's trained recommendation data.

It considers:

* Submitted code
* Programming language
* Similar known patterns
* Risk level
* Knowledge-base information

The advisor can return:

```text
Relevant finding
Risk-aware recommendations
Similarity information
Source
Source URL
```

Feedback can also be stored through the remediation feedback mechanism.

Implementation:

```text
backend/remediation_advisor_v2.py
backend/remediation_feedback.json
```

---

# 💬 7. Code Analysis Chat Assistant

The backend provides a chat endpoint that allows users to submit code-related questions and receive analysis based on the project's analysis capabilities.

The system can combine:

* Code analysis
* Knowledge retrieval
* Risk information
* Recommendations

This provides an assistant-style interface rather than requiring every analysis to be performed manually through individual scripts.

---

# 📊 8. Business Risk Analysis

Technical findings can also be translated into business-oriented information.

The business analysis layer provides:

### Operational Risk

Describes possible operational consequences of the finding.

### Financial Risk

Provides an estimated remediation and operational exposure description.

### Regulatory Risk

Highlights potential audit or compliance considerations.

The system also estimates remediation effort based on:

* Risk level
* Programming language
* Complexity

Example output fields include:

```text
engineering_days
sprints
resources
```

Implementation:

```text
backend/risk_analysis.py
```

---

# 🎯 9. Priority Calculation

Code findings can be prioritized using multiple risk factors:

```text
Severity
Business Impact
Technical Risk
Regulatory Risk
```

The priority calculation produces:

```text
score
priority
```

with priority levels:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

The calculation is configuration-driven rather than relying on a fixed response.

---

# 🏢 10. Enterprise Severity Scoring

The project includes a configurable severity-scoring layer.

The score considers factors including:

```text
Severity
Reachability
Production Exposure
Persistence
External Dependency
```

The resulting assessment includes:

```text
score
severity
factors
```

Configuration is stored separately in:

```text
backend/severity_scoring.json
```

and the scoring implementation is:

```text
backend/severity_scoring.py
```

This makes the scoring logic configurable without embedding all thresholds directly inside the API.

---

# 📋 11. Executive Briefing

The project includes an automated executive briefing generator.

It summarizes submitted findings using:

* Finding count
* Risk distribution
* Estimated engineering effort

For example, a collection of findings can be converted into a summary containing:

```text
Finding count
Risk distribution
Estimated engineering days
Executive briefing
```

Implementation:

```text
backend/executive_briefing.py
```

The briefing is generated dynamically from the submitted findings rather than being a static report.

---

# 📄 12. Automated Technical Report Generation

CodeGuard AI can generate a PDF technical assessment report.

The report can contain sections such as:

```text
Executive Summary
Risk Summary
Business Risk
Remediation Effort
Prioritized Findings
Roadmap
```

The report generator is implemented in:

```text
backend/report_generator.py
```

Generated reports are stored under:

```text
backend/reports/
```

Example:

```text
Y2038_Technical_Assessment_Report.pdf
```

---

# 🔐 13. Prompt Security and Sanitization

The project includes prompt sanitization to reduce the exposure of sensitive-looking identifiers in submitted text.

Example input:

```text
Analyze CLIENT_SECRET_PROJECT proprietary_timestamp for Y2038 risk
```

The sanitization layer can transform sensitive identifiers into a redacted form such as:

```text
Analyze [REDACTED_NAME]_PROJECT proprietary_timestamp for Y2038 risk
```

Implementation:

```text
backend/prompt_security.py
```

API endpoint:

```text
POST /sanitize
```

---

# 🤖 14. GitHub Pull Request Review Bot

CodeGuard AI includes a prototype GitHub PR review workflow.

The bot can:

1. Connect to a GitHub repository.
2. Read changed files from a pull request.
3. Identify supported source-code files.
4. Analyze the changed code.
5. Detect potential Y2038 risks.
6. Display risk and recommendation information.
7. Optionally post review information back to GitHub when configured.

The implementation uses environment variables for repository configuration rather than embedding credentials in source code.

Configuration variables include:

```text
GITHUB_TOKEN
GITHUB_OWNER
GITHUB_REPO
GITHUB_PR_NUMBER
GITHUB_POST_COMMENT
```

Implementation:

```text
backend/code_review_bot/
```

Main files:

```text
github_pr_review_bot.py
review_bot.py
test_github_review.py
test_y2038.c
```

A test PR was created using code containing:

```c
int timestamp = time(NULL);
```

and the review pipeline identified it as:

```text
Risk: HIGH
Suppressed: False
```

---

# 🧪 15. Case Study and Dataset Metrics

The project includes automated extraction of dataset-level metrics.

The extraction process reports:

```text
Total patterns:       500
Unique patterns:      497
High-risk findings:   213
Medium-risk findings: 106
Low-risk findings:    181
Unsafe findings:      319
Safe findings:        181
Recommendation coverage: 100%
Source coverage:         100%
Validation coverage:     100%
```

Language distribution:

```text
C:      232
Java:   209
C++:     59
```

These figures describe the project's dataset and validation artifacts. They should not be interpreted as production/client vulnerability statistics.

Generated files:

```text
backend/case_study_metrics.csv
backend/case_study_metrics.json
```

---

# 🧩 16. VS Code Extension Prototype

A VS Code extension prototype is included to bring CodeGuard AI analysis closer to the developer workflow.

The extension can:

* Read selected/open source code.
* Detect supported programming languages.
* Send code to the CodeGuard AI backend.
* Request analysis or remediation.
* Display the returned result inside VS Code.

Supported language mapping currently includes:

```text
C
C++
Java
```

Extension directory:

```text
vscode-extension/
```

Important files:

```text
extension.js
package.json
README.md
package-lock.json
codeguard-ai-y2038-0.1.0.vsix
```

The extension has also been packaged as a VSIX artifact.

---

# 🌐 REST API

The Flask backend exposes endpoints for the main analysis capabilities.

| Endpoint                   | Purpose                                        |
| -------------------------- | ---------------------------------------------- |
| `POST /analyze`            | Analyze source code and classify Y2038 risk    |
| `POST /remediate`          | Generate context-aware remediation             |
| `POST /feedback`           | Store remediation feedback                     |
| `POST /chat`               | Code analysis assistant interaction            |
| `POST /sanitize`           | Sanitize potentially sensitive prompt text     |
| `GET /prompts`             | Access the prompt library                      |
| `POST /severity-score`     | Calculate enterprise severity                  |
| `POST /executive-briefing` | Generate executive summary information         |
| `POST /business-analysis`  | Calculate business risk and remediation effort |
| `POST /generate-report`    | Generate technical assessment PDF              |
| `GET /`                    | Backend health/basic response                  |

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │     User / IDE      │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
              Web Interface    VS Code Extension   GitHub PR
                    │               │                │
                    └───────────────┼────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    Flask Backend    │
                         │       app.py        │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ML Risk Analyzer       False Positive          Knowledge Base
      TF-IDF + SVM             Classifier              Retrieval
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │  Risk Assessment    │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
       Remediation             Business Risk       Severity Scoring
       Engine + Advisor        + Effort Estimate       + Priority
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │ Reports / Briefing  │
                         └─────────────────────┘
```

---

# 📁 Project Structure

```text
Code-Analysis-Assistant-Y2K38/
│
├── README.md
├── COMPLETION_STATUS.md
├── Y2k38.ipynb
│
├── backend/
│   ├── app.py
│   ├── train_model.py
│   ├── train_false_positive.py
│   ├── test_false_positive.py
│   │
│   ├── svm_model.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── false_positive_model.pkl
│   ├── false_positive_vectorizer.pkl
│   ├── recommendation_dataset.pkl
│   │
│   ├── Y2038_Week1_Dataset_500_Unique_With_Recommendations.xlsx
│   ├── Y2038_Knowledge_Base_v2.xlsx
│   │
│   ├── rag_knowledge_base.py
│   ├── remediation_advisor_v2.py
│   ├── remediation_engine.py
│   ├── remediation_rules.json
│   ├── remediation_feedback.json
│   │
│   ├── risk_analysis.py
│   ├── risk_profiles.json
│   ├── severity_scoring.py
│   ├── severity_scoring.json
│   ├── executive_briefing.py
│   ├── prompt_security.py
│   ├── prompt_library.py
│   ├── prompt_library.json
│   ├── report_generator.py
│   │
│   ├── extract_case_study.py
│   ├── case_study_metrics.csv
│   ├── case_study_metrics.json
│   │
│   ├── code_review_bot/
│   │   ├── github_pr_review_bot.py
│   │   ├── review_bot.py
│   │   ├── test_github_review.py
│   │   └── test_y2038.c
│   │
│   └── reports/
│       └── Y2038_Technical_Assessment_Report.pdf
│
├── frontend/
│   ├── index.html
│   └── style.css
│
└── vscode-extension/
    ├── extension.js
    ├── package.json
    ├── package-lock.json
    ├── README.md
    └── codeguard-ai-y2038-0.1.0.vsix
```

---

# ⚙️ Technology Stack

### Backend

* Python
* Flask
* Flask-CORS
* Scikit-learn
* Joblib
* Pandas
* OpenPyXL
* ReportLab

### Machine Learning

* TF-IDF
* Linear SVM
* Secondary false-positive classifier
* Similarity-based recommendation retrieval

### Frontend

* HTML
* CSS
* JavaScript

### Developer Tooling

* VS Code Extension API
* GitHub Pull Request integration

### Data

* Excel-based Y2038 pattern dataset
* JSON configuration files
* Pickled ML models and vectorizers

# 👩‍💻 Author

**Bhagyashri Varape**

B.Tech — Electronics & Telecommunication Engineering

Project Repository:

https://github.com/Bhagyashriwarpe/Code-Analysis-Assistant-Y2K38
