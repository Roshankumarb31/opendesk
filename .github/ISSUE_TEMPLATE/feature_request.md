***
name: Feature request
description: Suggest an idea or enhancement for OpenDesk
title: "[Feature]: "
labels: ["enhancement"]
assignees: []

body:
- type: markdown
  attributes:
    value: |
      Thanks for your idea! Please provide details so we can evaluate it.

- type: input
  id: summary
  attributes:
    label: Summary
    description: A concise description of the feature.
    placeholder: e.g., "Add global hotkey to open OpenDesk"
  validations:
    required: true

- type: textarea
  id: problem
  attributes:
    label: Problem to solve
    description: What user problem or workflow does this feature address?
    placeholder: Describe the pain point or use case.
  validations:
    required: true

- type: textarea
  id: proposal
  attributes:
    label: Proposed solution
    description: How should OpenDesk behave? Any UI/UX suggestions?
    placeholder: Describe the flow, settings, and expected behavior.
  validations:
    required: true

- type: textarea
  id: alternatives
  attributes:
    label: Alternatives considered
    description: Have you thought of other ways to solve this?
  validations:
    required: false

- type: textarea
  id: mocks
  attributes:
    label: Visuals/Mockups
    description: Attach wireframes or screenshots if helpful.
  validations:
    required: false

- type: input
  id: priority
  attributes:
    label: Priority
    description: How important is this feature?
    placeholder: nice-to-have / important / critical
  validations:
    required: false

- type: textarea
  id: additional-context
  attributes:
    label: Additional context
    description: Anything else we should know?
  validations:
    required: false
***