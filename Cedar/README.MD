# Cedar Policy Language Demo

## Overview

This demo showcases Cedar, Amazon's open-source policy language for fine-grained authorization. Cedar uses automated reasoning to validate policies and make authorization decisions with mathematical certainty.

## Setup

### Prerequisites
- Rust toolchain installed
- Cedar CLI installed

### Installation Steps

1. **Install Rust:**
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source ~/.cargo/env
   ```

2. **Install Cedar CLI:**
   ```bash
   cargo install cedar-policy-cli
   ```

### Demo Files
Navigate to `cedar-cli/` directory containing:
- `schema.json` - Defines entity types and action structure
- `policy.cedar` - Authorization policies in Cedar language
- `entities.json` - Entity data (users, resources, groups)
- `request-allow.json` - Authorization request that should be allowed
- `request-deny.json` - Authorization request that should be denied

## Demo Scenarios

### 1. Policy Validation
Validate that policies conform to the schema:
```bash
cd cedar-cli/
cedar validate --policies policy.cedar --schema schema.json
```
**Expected Output:** `policy set validation passed`

### 2. Authorization Testing

**Test A - Deny Scenario:**
```bash
cedar authorize --policies policy.cedar --entities entities.json --request-json request-deny.json --schema schema.json
```
**Expected Result:** `DENY` - No policies match the request

**Test B - Allow Scenario:**
```bash
cedar authorize --policies policy.cedar --entities entities.json --request-json request-allow.json --schema schema.json
```
**Expected Result:** `ALLOW` - Request matches policy1

## Key Takeaways

- **Mathematical Certainty:** Cedar provides provable authorization decisions using automated reasoning
- **Schema Validation:** Policies are validated against schemas to prevent runtime errors
- **Fine-grained Control:** Supports complex authorization scenarios with attribute-based access control
- **Policy Testing:** Enables testing authorization scenarios before deployment
- **Open Source:** Cedar is open-source and can be integrated into any application
- **AWS Integration:** Powers Amazon Verified Permissions service for cloud-native applications

## Additional Resources
- [Cedar Policy Language Documentation](https://docs.cedarpolicy.com/)
- [Cedar GitHub Repository](https://github.com/cedar-policy/cedar)




