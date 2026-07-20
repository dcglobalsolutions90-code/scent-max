# scent-max

Cynthia AI agent architecture: a small set of reusable agent *type
templates*, each instantiated and parameterized many times at runtime
rather than hand-written per instance.

The full spec is in [`docs/AGENT_ARCHITECTURE.md`](docs/AGENT_ARCHITECTURE.md).
The implementation is the [`cynthia`](cynthia) package:

- `cynthia.base.Agent` — base class every template extends
- `cynthia.agents.*` — the 9 templates (Sensory, Motor/Interaction, Memory,
  Emotional Regulation, Decision-Making, Language & Communication, Social
  Cognition, Executive Function, Attention/Context)
- `cynthia.registry.AgentRegistry` — spawns and tracks N instances of a
  template
- `cynthia.bus.MessageBus` — pub/sub wiring between agent instances, keyed
  by role

## Usage

```python
from cynthia.agents import SensoryAgent, AttentionContextAgent
from cynthia.registry import AgentRegistry

registry = AgentRegistry()
cameras = registry.spawn(SensoryAgent, n=4, input_source_type="camera")
attention = registry.spawn(AttentionContextAgent, n=1, relevance_threshold=0.4)[0]
```

See `tests/test_pipeline.py` for a worked example that wires several
templates together over a `MessageBus`.

## Tests

```
python -m unittest discover -s tests
```
