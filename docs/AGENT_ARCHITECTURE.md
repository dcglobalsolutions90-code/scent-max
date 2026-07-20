# Cynthia AI — Agent Architecture Specification

## How to read this file

Real multi-agent AI systems are not built as billions of individually-written
agents. They are built as a small set of **agent type templates** (classes),
each instantiated many times and parameterized differently at runtime. This
spec defines 9 agent type templates. A coding tool can use each template
below to scaffold a class, then instantiate/replicate it as needed.

The corresponding implementation lives in [`cynthia/`](../cynthia), with one
module per template under [`cynthia/agents/`](../cynthia/agents).

-----

## 1. Sensory Agent

- **Role:** Ingest and interpret raw input (camera/vision, file/touch)
- **Inputs:** image/video frames, file system events
- **Outputs:** labeled objects, scene descriptions, file interaction events
- **Key params:** input source type, recognition confidence threshold

## 2. Motor / Interaction Agent

- **Role:** Execute actions and handle user-facing interaction (Jarvis-style)
- **Inputs:** decision agent output, user messages
- **Outputs:** natural language responses, system actions, UI events
- **Key params:** response tone, action permissions

## 3. Memory Agent

- **Role:** Store, organize, and retrieve information (short + long term)
- **Inputs:** learning agent output, context queries
- **Outputs:** retrieved facts/events, updated memory store
- **Key params:** retention policy, indexing method, recall relevance threshold

## 4. Emotional Regulation Agent

- **Role:** Assign value (good/bad) to outcomes and experiences
- **Inputs:** outcome events, explicit user feedback ("great job", "thank you")
- **Outputs:** reward/penalty signal
- **Key params:** reward weighting, user-feedback sensitivity

## 5. Decision-Making Agent

- **Role:** Evaluate options against goals and select actions
- **Inputs:** memory, context, reward signals
- **Outputs:** chosen action, confidence score
- **Key params:** goal set, risk tolerance

## 6. Language & Communication Agent

- **Role:** Parse input language, generate expressive output
- **Inputs:** raw text/speech
- **Outputs:** structured intent, generated language
- **Key params:** language model config, tone

## 7. Social Cognition Agent

- **Role:** Track relationships, read context, predict behavior
- **Inputs:** interaction history, user profile data
- **Outputs:** relationship map, predicted response
- **Key params:** social graph depth

## 8. Executive Function Agent

- **Role:** Plan, prioritize, and coordinate all other agents
- **Inputs:** all agent outputs
- **Outputs:** task schedule, coordination commands
- **Key params:** priority rules, oversight scope

## 9. Attention / Context Agent

- **Role:** Filter relevance, track cause-effect, maintain situational awareness
- **Inputs:** all incoming signals
- **Outputs:** filtered/prioritized signal stream
- **Key params:** relevance threshold, urgency weighting

-----

## Scaling note

"87 billion agents" is not a literal target for implementation — it was
useful as a conceptual mapping to neuron count, not a build spec. In
practice, each template above is instantiated N times (N = whatever your
compute budget and use case require), not written out individually. See
`cynthia.registry.AgentRegistry.spawn` for how instantiation/replication of
a template is done in code.
