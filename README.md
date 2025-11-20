# Automated Reasoning on AWS Workshop

## Overview

Automated reasoning is the field of computer science that attempts to provide assurance about what a system or program will do—or will never do—based on mathematical proof.

This workshop guides you through using automated reasoning tools available in the AWS ecosystem to answer questions about security policies and logic formulas. Specifically, this workshop covers:

1.  **AWS IAM Access Analyzer:** Validating Identity and Resource policies using AWS CLI.
2.  **Cedar Policy Language:** Writing and verifying authorization policies using the Cedar CLI.
3.  **Amazon Verified Permissions:** Building and deploying Cedar-based authorization systems with AWS services integration.
4.  **Amazon Bedrock Guardrails:** Implementing AI safety controls using automated reasoning for content filtering.

## Prerequisites

To execute this workshop successfully, you will need:

* **An AWS Account:** To generate IAM credentials.
* **AWS IAM Credentials:** An `Access Key ID` and `Secret Access Key` with permissions to run `accessanalyzer` commands.

## Environment Setup

### Python Environment
Ensure you have Python 3.8+ installed on your system. Create a virtual environment for the workshop:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### AWS CLI Installation and Configuration
Install and configure AWS CLI v2 to interact with AWS services. For detailed installation instructions, visit the [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

After installation, configure your credentials:
```bash
aws configure
```

### Cedar CLI Installation
Install the Cedar CLI for local policy validation and testing:

1. **Install Rust:** Visit [rustup.rs](https://rustup.rs/) for installation instructions
2. **Install Cedar CLI:**
   ```bash
   cargo install cedar-policy-cli
   ```

## Workshop Steps

### Part 1: IAM Access Analyzer

In this section, you will use the AWS CLI to mathematically validate IAM policies against specific security checks.

**Working Directory:** `/content/LAP_AutomatedReasoning/AccessAnalyzer`

### Part 2: Cedar Policy Language

In this section, you will set up the Cedar environment and use it to validate and authorize requests based on a custom schema.

**Working Directory:** `/content/LAP_AutomatedReasoning/Cedar/cedar-cli/`

### Part 3: Amazon Verified Permissions

In this section, you will deploy a complete authorization system using Amazon Verified Permissions (AVP) with Cedar policies, integrated with Cognito authentication and API Gateway.

**Working Directory:** `LAP_AutomatedReasoning/AVP/`

### Part 4: Amazon Bedrock Guardrails

In this section, you will explore Amazon Bedrock's automated reasoning capabilities through Guardrails, demonstrating how AI safety controls work with and without content filtering.

**Working Directory:** `LAP_AutomatedReasoning/Bedrock/`

## Repository Structure

The logic relies on the files cloned from `PaoloL/LAP_AutomatedReasoning`. The structure used in this workshop is:

```text
LAP_AutomatedReasoning/
├── AccessAnalyzer/
│   ├── check_access_not_granted_policy.json
│   ├── check_no_new_access_existing_policy.json
│   ├── check_no_new_access_updated_policy.json
│   ├── check_no_public_access_policy.json
│   └── validate_policy_document.json
├── Cedar/
│   └── cedar-cli/
│       ├── schema.json
│       ├── policy.cedar
│       ├── entities.json
│       ├── request-deny.json
│       └── request-allow.json
├── AVP/
│   ├── src/
│   │   ├── authorize/
│   │   │   ├── authorizer.py
│   │   │   └── requirements.txt
│   │   └── callback/
│   │       ├── callback.py
│   │       └── requirements.txt
│   ├── avp.yml
│   ├── cognito.yml
│   ├── lambda.yml
│   ├── main.yml
│   ├── README.MD
│   └── samconfig.toml
└── Bedrock/
    ├── travel_assistant.py
    ├── requirements.txt
    └── README.MD
