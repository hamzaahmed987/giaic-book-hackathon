# Claude Code Subagents

This directory contains Claude Code subagents designed for specific tasks in the AI Book Platform.

## Available Subagents

### 1. Chapter Generator (`chapter-generator.md`)

Generates book chapters from specifications using the Spec-Kit Plus methodology.

**Usage:**
```bash
# Use with Claude Code
claude-code --agent chapter-generator.md
```

**Prompt Format:**
```
Generate Chapter [N]: [Title]

Topics to cover:
- Topic 1
- Topic 2
- Topic 3

Prerequisites: [list prerequisites]
Target audience: [beginner/intermediate/advanced]
```

### 2. Spec Converter (`spec-converter.md`)

Converts raw specifications into structured book content.

**Usage:**
```bash
claude-code --agent spec-converter.md
```

### 3. Embedding Ingester (`embedding-ingester.md`)

Processes markdown files and stores embeddings in Qdrant.

**Usage:**
```bash
claude-code --agent embedding-ingester.md
```

### 4. QA Tester (`qa-tester.md`)

Tests generated content for quality, consistency, and accuracy.

**Usage:**
```bash
claude-code --agent qa-tester.md
```

## Agent Skills

Reusable skills that can be used across agents:

### Content Skills

- **explain-simply**: Simplify complex concepts for beginners
- **generate-examples**: Create practical code examples
- **create-exercises**: Design hands-on exercises
- **summarize-chapter**: Generate chapter summaries

### Technical Skills

- **validate-code**: Check code examples for correctness
- **check-links**: Verify all links in content are valid
- **lint-markdown**: Ensure markdown formatting is correct

## Creating New Subagents

1. Create a new `.md` file in this directory
2. Follow the template structure:

```markdown
# Agent: [Name]

## Purpose
[What this agent does]

## Capabilities
- [Capability 1]
- [Capability 2]

## System Prompt
[The system prompt for the agent]

## Example Interactions
[Show example uses]
```

## Integration with CI/CD

These subagents can be integrated into GitHub Actions:

```yaml
- name: Generate Chapter
  run: |
    claude-code --agent subagents/chapter-generator.md \
      --input "Generate Chapter 7: Advanced Topics"
```
