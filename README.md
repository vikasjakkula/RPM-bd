# Remote Patient Monitoring (IoT) Agent – Hackathon 2-Minute Pitch Guide

## 1. Problem Understanding & Relevance

Delays in detecting changes in patient vitals are deadly, especially for high-risk or remote patients. Globally, cardiovascular diseases (CVDs) caused 19.8 million deaths in 2022 (32% of all deaths), and 19.2 million in 2023, with 85% from heart attacks and strokes. In 2023, the US saw 915,973 CVD deaths—one every 34 seconds. In India, heart attack deaths rose to 32,457 in 2022. Manual monitoring leads to late interventions. Our solution: real-time, automated remote monitoring for rapid response.

## Tech stack (latest libraries)

- **Backend:** Flask 3, scikit-learn (LogisticRegression for heart risk), pandas, numpy, OpenAI SDK (optional LLM summary).
- **Frontend:** React 18, Recharts (line + scatter plots for vitals and BP), Vite, Tailwind.

## 2. Solution Approach & Design Clarity

Our solution is a Python-based Remote Patient Monitoring (RPM) agent built on Flask. We create a mock IoT data stream that simulates live patient vitals such as heart rate and blood pressure. This data is processed in real-time by our backend, which continuously checks vital signs against configurable safety thresholds. If dangerous levels are detected, the system instantly triggers an emergency workflow—demonstrating end-to-end automation. All data, alerts, and controls are accessible via a REST API, enabling integration with a real-time vitals dashboard for clinicians.

**Key Deliverables:**
- **RPM agent:** Continuously ingests and analyzes vital sign data.
- **Dashboard:** Visualizes vitals and alerts in real-time.
- **Emergency alert demo:** Instantly notifies on threshold breaches.
- **Config system:** Adaptable thresholds for flexible deployment.

## 3. Innovation & Creativity

- **Real-time Automation:** Immediate detection and automated action, minimizing human delay.
- **Mock IoT Stream:** Rapid prototyping and extensibility for multiple sensor types.
- **Threshold Configuration:** User-adjustable; supports diverse patient needs and scenarios.
- **API-first Design:** Ready for integration with existing healthcare systems or for extension with AI-driven analytics.

## Git sync (backend + frontend)

This repo is pushed to `https://github.com/vikasjakkula/RPM-bd.git`. After committing, **push** so other devices get your changes:

```bash
git push origin main
```

On a **cloned device**, get the latest commits with:

```bash
git pull origin main
```

If you have the full RPM project, use `./scripts/push-all.sh` and `./scripts/pull-all.sh` from the project root (see `GIT_WORKFLOW.md`).

## Summary

This RPM agent rapidly detects high-risk health events, shortens emergency response times, and provides clinicians with always-on, real-time oversight—delivering measurable impact in just 24 hours. Our architecture is simple, scalable, and hackathon-ready for further innovations like AI integration or hardware prototyping.

