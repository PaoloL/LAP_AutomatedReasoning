# Cedar CLI 

## Files Structure

The project contains several files:

| File                | Purpose                                             |
|---------------------|-----------------------------------------------------|
| `policy.cedar`      | Contains the Cedar policies for authorization.      |
| `schema.json`       | Defines the schema                                  |
| `entities.json`     | Lists all entities (users, bikes, actions) and attributes. |
| `request-allow.json`| Authorization request expected to result in **ALLOW**.|
| `request-deny.json` | Authorization request expected to result in **DENY**.|

---

## CLI available Commands

The following commands are available using the Cedar CLI:

| Command | Purpose | What it Evaluates | When to Use |
|---------|---------|-------------------|-------------|
| `cedar validate` | Validates policies against the schema | Checks syntax and schema compliance of policies | When writing or updating policies
| `cedar evaluate` | Evaluates a single expression | Expressions only (e.g., principal.vendor == true) | When testing conditions or attributes logic without a policy file
| `cedar authorize` | Runs a full authorization request against policies | Policies + request + entities + schema | When performing authorization decisions (ALLOW/DENY)

---

## Example 1. **Validate Policies Against Schema**

```bash
cedar validate  --schema-format json --schema schema.json --policies policy.cedar
```

## Example 2. **Authorize Request Against Policies**

Expected Result: ALLOW

```bash
cedar authorize --policies policy.cedar --entities entities.json --request-json request-allow.json -v
```

Expected Result: DENY

```bash
cedar authorize --policies policy.cedar --entities entities.json --request-json request-deny.json -v
```

## Example 3. **Evaluate Expression**
Evaluate expressions directly from the command line:

```bash
cedar evaluate "principal.vendor == true" --entities entities.json --request-json request-allow.json
```

## Example 4. **More Complex Expression:

```bash
cedar evaluate "principal.vendor == true && resource.pricing > 8000" --entities entities.json --request-json request-allow.json
```