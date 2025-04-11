# <a id="OopCoreManageKnowledge"></a>OOP-core: Object-Oriented Knowledge Management System
```yaml
concept: OopCore
action: Manage
reaction: Knowledge
author: Claude AI (Anthropic)
reference: https://claude.ai/chat/4a2101af-e9e2-4274-bcb1-1195b9358f16
date: 2025-04-11
status: draft
tags: [documentation, overview, readme]
filepath: OOP-core/README.md
```

> **"What is well conceived is clearly stated,
> And the words to say it flow with ease."** - Nicolas Boileau

## Overview

OOP-core is a knowledge modeling and management framework based on object-oriented programming principles. It enables structuring, organizing, and manipulating concepts as objects with inheritance, encapsulation, and semantic polymorphism.

This system has been designed to address the needs of various domains (education, research, development) by providing a unified structure for representing concepts and their relationships.

## <a id="OopCoreStructureProject"></a>Project Structure
```yaml
concept: OopCore
action: Structure
reaction: Project
```

The project follows a Domain-Driven Design architecture:

```
OOP-core/
├── concepts/             # Concept definitions
│   ├── core/             # Core concepts (OOP-core-concept-20250411.json)
│   ├── inheritance/      # Inheritance-related concepts (OOP-inheritance-2024.json)
│   └── templates/        # Concept templates (*.jinja files)
├── infrastructure/       # Technical tools
│   ├── persistence/      # Concept storage (JSON, DB)
│   ├── search/           # Indexing and search (dynamic_tag_indexing_system.py)
│   └── generation/       # Document generation (create_document.py)
├── interfaces/           # User interfaces
│   ├── cli/              # Command-line interface
│   └── viewer/           # Concept visualization
├── scripts/              # Utility scripts (environment activation)
└── docs/                 # Documentation
```

> **Note**: The project is currently being reorganized from its original structure to this more domain-focused architecture.

## <a id="OopCoreDefineComponents"></a>Core Components
```yaml
concept: OopCore
action: Define
reaction: Components
```

### <a id="OopCoreModelConcepts"></a>1. Concept Modeling
```yaml
concept: OopCore
action: Model
reaction: Concepts
```

The core concepts are defined in JSON format:
- `OOP-core-concept-20250411.json`: Defines the fundamental structure
- `OOP-inheritance-2024.json`: Implements inheritance relationships

Each concept includes:
- **Unique Identifiers**: Each concept has a unique ID (e.g., `OOP-core-concept-2025`)
- **Rich Metadata**: Tags, contexts, expertise levels, domains
- **Hierarchical Relationships**: Support for inheritance between concepts
- **Multidimensional Tagging**: Classification along multiple facets

Example structure:
```json
{
  "concept": {
    "id": "OOP-core-concept-2025",
    "name": "Fundamental concept of object-oriented programming",
    "meta": {
      "paradigm": "Smalltalk",
      "version": "2.1"
    },
    "tags": [...],
    "context": {...},
    "expertise": {...},
    "domain": {...}
  }
}
```

### <a id="OopCoreIndexTags"></a>2. Dynamic Tag Indexing System
```yaml
concept: OopCore
action: Index
reaction: Tags
```

The `dynamic_tag_indexing_system.py` provides a sophisticated mechanism for:
- Building hierarchical relationships between tags
- Supporting different relation types (parent_of, related_to, prerequisite_for)
- Enabling semantic search across concepts
- Indexing documents with their associated tags

### <a id="OopCoreGenerateDocuments"></a>3. Document Generation System
```yaml
concept: OopCore
action: Generate
reaction: Documents
```

The document generation system (`create_document.py`):
- Transforms concept definitions into actual documents
- Applies templates based on the target format (Python, Markdown, etc.)
- Preserves inheritance relationships between concepts
- Adapts content based on context and audience

### <a id="OopCoreConfigureEnvironment"></a>4. Cross-Platform Environment Configuration
```yaml
concept: OopCore
action: Configure
reaction: Environment
```

Tools to activate the development environment on different platforms:
- **Git Bash / WSL / Linux**: Via `scripts/activate.sh`
- **Windows CMD**: Via `scripts\activate.bat`
- **PowerShell**: Via `scripts\activate.ps1`

## <a id="OopCoreExplainUsage"></a>Usage
```yaml
concept: OopCore
action: Explain
reaction: Usage
```

### <a id="OopCoreInstallSystem"></a>Installation
```yaml
concept: OopCore
action: Install
reaction: System
```

1. Clone the repository:
   ```bash
   git clone https://github.com/EricVBogaert/OOP-core-Datura.git
   cd OOP-core
   ```

2. Activate the virtual environment:
   ```bash
   # On Linux/WSL/Git Bash
   source scripts/activate.sh
   
   # On Windows CMD
   scripts\activate.bat
   
   # On PowerShell
   . .\scripts\activate.ps1
   ```

### <a id="OopCoreCreateConcept"></a>Creating a New Concept
```yaml
concept: OopCore
action: Create
reaction: Concept
```

1. Define your concept in JSON following the model in `concepts/core/OOP-core-concept-20250411.json`
2. Use inheritance to extend existing concepts
3. Add appropriate tags, contexts, and relationships

### <a id="OopCoreGenerateDocument"></a>Document Generation
```yaml
concept: OopCore
action: Generate
reaction: Document
```

Use `create_document.py` to generate documents from concepts:

```bash
python infrastructure/generation/create_document.py --concept-id <ID> --template <TEMPLATE> --output <o>
```

### <a id="OopCoreSearchNavigate"></a>Search and Navigation
```yaml
concept: OopCore
action: Search
reaction: Navigate
```

The indexing system allows searching for concepts by:
- Tags (single or multiple)
- Context (education, research, development)
- Expertise level (beginner, intermediate, advanced...)
- Domain (computer science, biology, mathematics...)

## <a id="OopCoreDescribePrinciples"></a>Key Concepts
```yaml
concept: OopCore
action: Describe
reaction: Principles
```

1. **Semantic Polymorphism**: The same concept can be interpreted differently depending on context
2. **Structure Inheritance**: Documents inherit properties from parent concepts
3. **Adaptive Contextualization**: Content adapts to expertise level and context
4. **Multidimensional Tagging**: Classification along multiple simultaneous facets

## <a id="OopCoreIntegrateClaude"></a>Claude AI Integration
```yaml
concept: OopCore
action: Integrate
reaction: Claude
```

The system integrates with Claude AI for:
- Concept-based content generation
- Knowledge extraction and structuring
- Template and document enhancement

## <a id="OopCorePlanDevelopment"></a>Future Development
```yaml
concept: OopCore
action: Plan
reaction: Development
```

- Web user interface for concept exploration
- Graphical visualization of concept relationships
- REST API for accessing concepts from other applications
- Collaborative tools for concept editing

## <a id="OopCoreExplainPhilosophy"></a>History and Philosophy
```yaml
concept: OopCore
action: Explain
reaction: Philosophy
```

This project draws inspiration from the Smalltalk philosophy where "everything is an object," applying it to knowledge management. The structured approach allows for a clear organization of concepts while maintaining the flexibility needed to adapt to different domains and contexts.

## <a id="OopCoreProvideContact"></a>Contact
```yaml
concept: OopCore
action: Provide
reaction: Contact
```

Developed at UCLouvain (Louvain-la-neuve, Belgium)

---

*This document is generated from the concept `OOP-core-concept-2025`*