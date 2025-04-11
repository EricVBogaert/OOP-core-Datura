# <a id="OopCoreDefineStandards"></a>OOP-core Project Standards
```yaml
concept: OopCore
action: Define
reaction: Standards
author: Claude AI (Anthropic)
reference: https://claude.ai/chat/4a2101af-e9e2-4274-bcb1-1195b9358f16
date: 2025-04-11
status: draft
tags: [standards, documentation, formatting, conventions]
filepath: OOP-core/docs/standards.md
```

## <a id="OopCoreStandardizeDocumentation"></a>File and Documentation Standards
```yaml
concept: OopCore
action: Standardize
reaction: Documentation
```

### <a id="OopCoreFormatHeaders"></a>HTML Anchors and YAML Metadata
```yaml
concept: OopCore
action: Format
reaction: Headers
```

All Markdown files in the OOP-core project should include an HTML anchor element and YAML metadata block:

```markdown
# <a id="ConceptActionReaction"></a>Document Title
```yaml
concept: PascalCaseConcept
action: PascalCaseAction
reaction: PascalCaseReaction
author: Author Name
reference: https://reference-url-if-applicable
date: YYYY-MM-DD
status: draft|review|approved|deprecated|todo
tags: [tag1, tag2, tag3]
filepath: relative/path/to/file.md
```

Document content starts here...
```

For Python files, use a commented block in the docstring:

```python
"""
# <a id="ConceptActionReaction"></a>Module Title
```yaml
concept: PascalCaseConcept
action: PascalCaseAction
reaction: PascalCaseReaction
author: Author Name
reference: https://reference-url-if-applicable
date: YYYY-MM-DD
status: draft|review|approved|deprecated|todo
tags: [tag1, tag2, tag3]
filepath: relative/path/to/file.py
```

Module documentation follows...
"""

# Code starts here
```

For shell scripts:

```bash
#!/bin/bash
# <a id="ConceptActionReaction"></a>Script Title
# ```yaml
# concept: PascalCaseConcept
# action: PascalCaseAction
# reaction: PascalCaseReaction
# author: Author Name
# reference: https://reference-url-if-applicable
# date: YYYY-MM-DD
# status: draft|review|approved|deprecated|todo
# tags: [tag1, tag2, tag3]
# filepath: relative/path/to/script.sh
# ```

# Script content starts here
```

### <a id="OopCoreStructureIdentifiers"></a>Concept-Action-Reaction Structure
```yaml
concept: OopCore
action: Structure
reaction: Identifiers
```

The `ConceptActionReaction` naming follows the PascalCase pattern:

1. **Concept**: The domain, entity, or object being addressed (e.g., `OopCore`)
2. **Action**: The operation or process being performed (e.g., `Define`, `Model`, `Index`)
3. **Reaction**: The expected outcome or result (e.g., `Standards`, `Concepts`, `Tags`)

Examples:
- `OopCoreModelConcepts`: Modeling of core concepts
- `OopCoreIndexTags`: Indexing and organization of tags
- `OopCoreGenerateDocuments`: Document generation from concepts

This naming scheme:
- Provides navigation anchors for jumping between sections
- Creates semantic relationships between related components
- Enables traceability in documentation
- Facilitates searching and indexing
- Avoids confusion with kebab-case content in identifiers

### <a id="OopCoreSpecifyMetadata"></a>Required Metadata Fields
```yaml
concept: OopCore
action: Specify
reaction: Metadata
```

- **concept**: Name of the primary concept being addressed
- **action**: Specific action being performed
- **reaction**: Expected outcome or result
- **author**: Name of the author or contributor
- **date**: Date of creation or last significant modification (YYYY-MM-DD format)
- **status**: Current status of the document
- **filepath**: Relative path of the file within the project structure

### <a id="OopCoreAddOptionalFields"></a>Optional Metadata Fields
```yaml
concept: OopCore
action: Add
reaction: OptionalFields
```

- **reference**: URL or identifier of any reference material or discussion
- **version**: Version number if applicable
- **tags**: Array of relevant tags
- **dependencies**: Other files or components this file depends on
- **examples**: Links to example implementations
- **related**: Related concepts or files

### <a id="OopCoreDefineStatuses"></a>Status Values
```yaml
concept: OopCore
action: Define
reaction: Statuses
```

- **draft**: Initial creation, not yet complete
- **review**: Ready for peer review
- **approved**: Reviewed and approved for use
- **deprecated**: Still available but scheduled for removal
- **todo**: Placeholder for future implementation

## <a id="OopCoreStandardizeCode"></a>Code Standards
```yaml
concept: OopCore
action: Standardize
reaction: Code
```

### <a id="OopCoreFormatPython"></a>Python
```yaml
concept: OopCore
action: Format
reaction: Python
```

- Use PEP 8 style guide
- Document all functions, classes, and modules with docstrings
- Add type hints for parameters and return values
- Maximum line length: 100 characters
- File encoding: UTF-8
- Use relative imports within the package

### <a id="OopCoreFormatJson"></a>JSON
```yaml
concept: OopCore
action: Format
reaction: Json
```

- Use 2-space indentation
- Keys in camelCase or snake_case (be consistent within a file)
- Include a schema reference where applicable
- UTF-8 encoding

### <a id="OopCoreFormatTemplates"></a>Templates
```yaml
concept: OopCore
action: Format
reaction: Templates
```

- Document all variables used in templates
- Provide examples of expected output
- Use consistent naming conventions for variables

## <a id="OopCoreStandardizeCommits"></a>Commit Message Standards
```yaml
concept: OopCore
action: Standardize
reaction: Commits
```

Format:
```
[area]: Short summary (50 chars)

More detailed explanation if necessary. Wrap at 72 characters.
Explain what and why, not how (the code shows that).

References: #123, #456
```

Areas:
- **core**: Core concept model changes
- **infra**: Infrastructure changes
- **ui**: User interface changes
- **docs**: Documentation updates
- **test**: Test additions or changes
- **refactor**: Code refactoring without functionality changes

## <a id="OopCorePlanImplementation"></a>Implementation Plan
```yaml
concept: OopCore
action: Plan
reaction: Implementation
```

1. Create templates for different file types
2. Add pre-commit hooks to validate metadata blocks and anchors
3. Update existing files gradually to comply with standards
4. Document standards in project wiki or developer guide
5. Develop tooling to verify compliance and generate reports