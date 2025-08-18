***
name: Bug report
description: File a bug/issue to help us improve OpenDesk
title: "[Bug]: "
labels: ["bug"]
assignees: []

body:
- type: markdown
  attributes:
    value: |
      Thanks for taking the time to fill out this bug report!

- type: input
  id: summary
  attributes:
    label: Summary
    description: A short description of the bug.
    placeholder: e.g., "OpenDesk crashes when launching 'Close All'"
  validations:
    required: true

- type: textarea
  id: steps-to-reproduce
  attributes:
    label: Steps to reproduce
    description: How can we reproduce the behavior?
    placeholder: |
      1. Open OpenDesk
      2. Add an app item with type "Website"
      3. Click "Launch Selected"
      4. Observe error
  validations:
    required: true

- type: textarea
  id: expected-behavior
  attributes:
    label: Expected behavior
    description: What did you expect to happen?
  validations:
    required: true

- type: textarea
  id: actual-behavior
  attributes:
    label: Actual behavior
    description: What actually happened?
  validations:
    required: true

- type: textarea
  id: screenshots
  attributes:
    label: Screenshots/Recordings
    description: If applicable, add screenshots or a short screen recording.
  validations:
    required: false

- type: input
  id: opendesk-version
  attributes:
    label: OpenDesk version/build
    description: Include EXE name or commit hash if running from source.
    placeholder: e.g., OpenDesk_v1.0.0.exe or commit abc123
  validations:
    required: true

- type: input
  id: os
  attributes:
    label: OS version
    description: Windows version/build.
    placeholder: e.g., Windows 11 23H2
  validations:
    required: true

- type: checkboxes
  id: browsers
  attributes:
    label: Affected browsers (if website launching issue)
    options:
      - label: Chrome
      - label: Edge
      - label: Brave
      - label: Firefox
  validations:
    required: false

- type: textarea
  id: logs
  attributes:
    label: Logs or console output
    description: Paste any relevant logs or error messages.
    render: shell
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