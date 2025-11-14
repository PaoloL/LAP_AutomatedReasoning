# Check Access Not Granted

## Descriptiopn
Checks whether the specified access isn’t allowed by a policy.

Command Line Reference:
https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/check-access-not-granted.html


## Example

PASS Example - The following example checks if an IAM user has permission to delete and get bucket location of a S3 Bucket.

```bash
aws accessanalyzer check-access-not-granted \
    --policy-document file://check_access_not_granted_policy.json \
    --access actions="s3:DeleteBucket","s3:GetBucketLocation" \
    --policy-type IDENTITY_POLICY
```

FAILS Example - The following example checks if an IAM user has permission to delete and get bucket location of a S3 Bucket.

```bash
aws accessanalyzer check-access-not-granted \
    --policy-document file://access_not_granted_policy.json \
    --access actions="s3:GetObject" \
    --policy-type IDENTITY_POLICY
```

# Check No New Access

## Descriptiopn
Checks whether new access is allowed for an updated policy when compared to the existing policy.

Command Line Reference:
https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/check-no-new-access.html

## Example

PASS Example - The following example checks if there are any changes in permissions between two policies. 
The first policy allows read-only access, while the second one grants full control over the resource. 

```bash
aws accessanalyzer check-no-new-access \
    --existing-policy-document file://check_no_new_access_existing_policy.json \
    --new-policy-document file://check_no_new_access_updated_policy.json \
    --policy-type IDENTITY_POLICY
```

# Check No Public Access

## Description
Checks whether public access is allowed by a policy.

Command Line Reference:
https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/check-no-public-access.html

## Example

PASS Example - The following example checks if an IAM role has public access.

```bash
aws accessanalyzer check-no-public-access \
    --policy-document file://check_no_public_access_policy.json \
    --resource-type AWS::S3::Bucket
```

# Validate Policy

## Description
Validates that a policy document adheres to the syntax requirements and security best practices

Command Line Reference:
https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/validate-policy.html

## Example

PASS Example - The following example validates a policy document.
```bash
aws accessanalyzer validate-policy \
    --policy-document file://validate_policy_document.json \
    --policy-type RESOURCE_POLICY
```

# Generate Policy from Beahviour

## Description
Generates a policy based on behavior analysis results.

Command Line Reference:
https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/start-policy-generation.html
https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/get-generated-policy.html

## Example
(TBD)

# Other IAM Access Analyzer examples using AWS CLI
https://docs.aws.amazon.com/code-library/latest/ug/cli_2_accessanalyzer_code_examples.html
