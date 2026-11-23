# BA Portfolio

Single-page portfolio with animated, interactive charts built from the real outputs of each case-study repo.

```bash
# from business-analyst/: run the analyses, then build
python projects/ach-return-rate-reduction/generate_data.py && python projects/ach-return-rate-reduction/analyze.py
python projects/card-dispute-backlog/generate_data.py && python projects/card-dispute-backlog/analyze.py
(cd projects/payment-reconciliation-breaks && python analysis.py)
(cd projects/claim-denial-root-cause && python analysis.py)
(cd projects/account-onboarding-funnel && python analysis.py)
python portfolio/build.py   # writes portfolio/index.html
```

Set `GH_USER` near the bottom of `src/template.html`, rebuild, and publish with GitHub Pages (Settings → Pages → Deploy from branch `main`, folder `/`).
