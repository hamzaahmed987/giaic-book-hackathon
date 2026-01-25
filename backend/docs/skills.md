# Agent Skills

Reusable skills that can be used across Claude Code subagents for the AI Book Platform.

## Content Skills

### 1. Explain Simply

**Purpose:** Simplify complex concepts for beginners.

**Prompt Template:**
```
Explain the following concept in simple terms for someone new to programming:

Concept: {concept}

Requirements:
- Use everyday analogies
- Avoid jargon (or explain it if necessary)
- Include a simple example
- Maximum 3 paragraphs
```

**Example:**
```
Input: "Explain vector embeddings"

Output:
"Think of embeddings like translating words into GPS coordinates. Just like
how GPS coordinates (latitude, longitude) tell you where something is in
physical space, embeddings tell you where a word or sentence is in 'meaning
space.'

Words with similar meanings end up close together. For example, 'dog' and
'puppy' would have similar coordinates, while 'dog' and 'refrigerator' would
be far apart.

Here's a simple visualization:
- 'happy' → [0.8, 0.9, 0.2]
- 'joyful' → [0.7, 0.85, 0.25]  ← Similar!
- 'sad' → [0.1, 0.2, 0.8]       ← Very different"
```

---

### 2. Generate Examples

**Purpose:** Create practical code examples for concepts.

**Prompt Template:**
```
Generate a practical code example for:

Concept: {concept}
Language: {python|javascript|typescript}
Level: {beginner|intermediate|advanced}

Requirements:
- Complete, runnable code
- Clear comments
- Expected output
- Common use case
```

**Example:**
```
Input: Concept="API rate limiting", Language="python", Level="intermediate"

Output:
```python
# Rate limiting with exponential backoff
import time
from functools import wraps

def rate_limit(max_calls: int, period: int):
    """
    Decorator that limits function calls.

    Args:
        max_calls: Maximum calls allowed in period
        period: Time period in seconds
    """
    calls = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls outside the period
            calls[:] = [t for t in calls if now - t < period]

            if len(calls) >= max_calls:
                sleep_time = period - (now - calls[0])
                print(f"Rate limit hit. Waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                calls.clear()

            calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@rate_limit(max_calls=3, period=10)
def call_api():
    print("API called!")

# Test
for i in range(5):
    call_api()

# Output:
# API called!
# API called!
# API called!
# Rate limit hit. Waiting 10.0s...
# API called!
# API called!
```
```

---

### 3. Create Exercises

**Purpose:** Design hands-on exercises to reinforce learning.

**Prompt Template:**
```
Create an exercise for:

Topic: {topic}
Difficulty: {⭐|⭐⭐|⭐⭐⭐}
Prerequisites: {list of concepts}

Requirements:
- Clear task description
- Starter code (if applicable)
- Hints (collapsible)
- Complete solution
- Expected output
```

---

### 4. Summarize Chapter

**Purpose:** Generate concise chapter summaries.

**Prompt Template:**
```
Summarize the following chapter content:

Content: {chapter_content}

Generate:
1. Key concepts table (3-5 rows)
2. Quick reference code snippet
3. Common mistakes to avoid (2-3 items)
4. One-sentence takeaway
```

---

## Technical Skills

### 5. Validate Code

**Purpose:** Check code examples for correctness.

**Prompt Template:**
```
Validate the following code:

```{language}
{code}
```

Check for:
- Syntax errors
- Logic errors
- Security issues
- Best practice violations
- Missing error handling

Return:
- Status: PASS | FAIL | WARNING
- Issues found (if any)
- Suggested fixes
```

---

### 6. Check Links

**Purpose:** Verify all links in content are valid.

**Prompt Template:**
```
Check all links in the following content:

{content}

For each link, verify:
- Internal links resolve to existing pages
- External links are accessible
- Anchor links (#section) point to valid headings

Return:
- Total links checked
- Valid links
- Broken links (with suggested fixes)
```

---

### 7. Lint Markdown

**Purpose:** Ensure markdown formatting is correct.

**Prompt Template:**
```
Lint the following markdown/MDX content:

{content}

Check for:
- Proper heading hierarchy (h1 → h2 → h3)
- Code block language tags
- Alt text for images
- Consistent list formatting
- Proper spacing

Return:
- Issues found with line numbers
- Suggested fixes
```

---

## Personalization Skills

### 8. Adapt for Level

**Purpose:** Adjust content for different skill levels.

**Prompt Template:**
```
Adapt the following content for a {beginner|intermediate|advanced} learner:

Content: {content}

For beginners:
- Add more context and explanations
- Include analogies
- Simplify code examples

For intermediate:
- Balance theory and practice
- Add edge cases

For advanced:
- Focus on nuances and optimization
- Include advanced patterns
```

---

### 9. Add Language Context

**Purpose:** Add comparisons to known programming languages.

**Prompt Template:**
```
The user knows: {known_languages}

Add relevant comparisons when explaining:
{concept}

For example, if they know JavaScript, compare Python's list comprehensions
to JavaScript's map/filter.
```

---

## Usage in Subagents

Skills can be composed in subagents:

```markdown
# Using Skills in Chapter Generator

1. Use "Generate Examples" skill for each concept
2. Use "Create Exercises" skill for practice section
3. Use "Summarize Chapter" skill for summary section
4. Use "Validate Code" skill before finalizing
```

## Skill Chaining Example

```
Input: Create personalized content about "API Authentication"

1. → Explain Simply (base explanation)
2. → Adapt for Level (based on user profile)
3. → Add Language Context (if user knows specific languages)
4. → Generate Examples (personalized examples)
5. → Validate Code (ensure correctness)
6. → Output: Personalized, validated content
```
