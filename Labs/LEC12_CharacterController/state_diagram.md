# Boy State Machine

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> idle: update / advance idle frame (0-7)
```