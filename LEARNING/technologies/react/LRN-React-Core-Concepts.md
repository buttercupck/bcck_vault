---
silo: LEARNING
category: React
type: Core-Concepts
version: 1.0
---

# LRN-React-Core-Concepts

React is a JavaScript framework for building dynamic UIs. Learning its basics will help you understand how data flows in modern apps, identify client-side vulnerabilities, and test component behavior effectively.

## Core Concepts:
- **Components** - Reusable UI elements
- **Props** - Data passed to components
- **State** - Component internal data
- **Data Flows** - How data moves through the application

## React Hooks:

### useMemo Hook
```javascript
const languageId = useMemo(() => (
    firstClientRequest?.language_id
    ?? firstClientRequest?.language?.id
    ?? firstClientRequest?.languages?.id
    ?? null
  ), [firstClientRequest]);
```

**`useMemo(() => ... , [firstClientRequest])`**: This React hook recalculates the `languageId` only if `firstClientRequest` itself changes. Otherwise, it uses the cached value. It's like writing down the answer to a math problem so you don't have to solve it again every time someone asks.

**Logic Flow**: 
1. First try to find `firstClientRequest.language_id`
2. If it doesn't exist, try to get `firstClientRequest.language.id`
3. If that doesn't exist, try to get `firstClientRequest.languages.id`
4. If none exist, resort to `null`

## Security Considerations:
- Input validation in components
- State management security
- Client-side data handling

## Cross-References:
- [[LRN-JavaScript-Core-Concepts]]
- [[LRN-N8N-React-Integration]]
- [[INC-Interlingo-Frontend-Architecture]]

---
*Migrated from legacy structure: 2025-09-16*