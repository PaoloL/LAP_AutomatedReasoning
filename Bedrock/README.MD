# Amazon Bedrock Guardrails Demo

## Overview

This demo showcases Amazon Bedrock's automated reasoning capabilities through Guardrails, which provide safety controls for generative AI applications. Bedrock Guardrails use automated reasoning to evaluate and filter content based on predefined policies, ensuring responsible AI usage.

## Setup

### Prerequisites
- AWS CLI configured with appropriate permissions
- Python 3.8+ installed
- Access to Amazon Bedrock and Nova Micro model
- Bedrock Guardrails policy already created (referenced in demo)

### Installation
```bash
pip install boto3
```

### Demo Files
- `travel_assistant.py` - Python application demonstrating guardrails scenarios
- `requirements.txt` - Python dependencies

## Demo Scenarios

This demo simulates a travel assistant chatbot with two scenarios:

### 1. Guardrails Disabled
- Direct interaction with Amazon Nova Micro model
- No content filtering or safety controls
- Shows raw model responses

### 2. Guardrails Enabled
- Uses existing guardrails policy: `arn:aws:bedrock:eu-west-1:767828734903:guardrail/spi7qw5ij0ch`
- Applies automated reasoning for content safety
- Demonstrates how guardrails filter inappropriate content

## Running the Demo

```bash
python travel_assistant.py
```

The application will demonstrate both scenarios with the same user input, showing the difference between protected and unprotected AI interactions.

## Key Takeaways

- **Automated Safety:** Bedrock Guardrails use automated reasoning to ensure AI safety without manual intervention
- **Content Filtering:** Policies automatically detect and filter harmful, biased, or inappropriate content
- **Responsible AI:** Enables deployment of AI applications with built-in safety controls
- **Policy-Based Control:** Centralized guardrails policies can be applied across multiple AI applications
- **Real-time Protection:** Sub-millisecond evaluation of content for immediate safety decisions
- **Compliance Ready:** Helps meet regulatory and organizational requirements for AI governance

## Additional Resources
- [Amazon Bedrock Guardrails Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
- [Amazon Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [Responsible AI with Amazon Bedrock](https://aws.amazon.com/bedrock/responsible-ai/)