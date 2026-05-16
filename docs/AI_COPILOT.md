# ThreatScope AI Copilot

ThreatScope is an explainable AI-driven SIEM for cyber threat intelligence.

The AI Copilot layer turns raw alerts into different levels of explanation:

- Executive brief: business impact, current protection, decision needed
- SOC analyst view: evidence, MITRE ATT&CK mapping, process chain
- Incident response view: containment and next actions
- Beginner mode: plain-English cyber explanations

The current demo uses local deterministic AI logic so it works offline on GitHub Pages.
The interface is structured so a real LLM API can later receive:

- selected incident
- evidence pack
- MITRE technique
- risk score
- confidence score
- user persona
- analyst question

This keeps the demo accessible while preserving a clean path toward production AI integration.
