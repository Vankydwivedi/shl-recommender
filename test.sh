#!/bin/bash
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"messages": [{"role": "user", "content": "I need an assessment for a Java developer"}, {"role": "assistant", "content": "Could you please specify the seniority level?"}, {"role": "user", "content": "Mid-level, around 4 years experience, works with stakeholders"}]}'
