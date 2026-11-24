"""Build index.html from src/template.html + each project's results.json.

    python build.py      (run the project analyses first)
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
P = HERE.parent / "projects"
ach = json.loads((P / "ach-return-rate-reduction/results/results.json").read_text())
dsp = json.loads((P / "card-dispute-backlog/results/results.json").read_text())
recon = json.loads((P / "payment-reconciliation-breaks/results.json").read_text())
denial = json.loads((P / "claim-denial-root-cause/results.json").read_text())
funnel = json.loads((P / "account-onboarding-funnel/results.json").read_text())
ml = json.loads((P / "customer-attrition-model/results/results.json").read_text())
ai = json.loads((P / "complaint-triage-ai/results/results.json").read_text())
inv = json.loads((P / "portfolio-drift-risk-monitor/results/results.json").read_text())

sim = ach["05_rule_simulation"][0]
drivers = {(r["intake"], r["routing"]): r for r in dsp["02_delay_drivers"]}
mm, mr = drivers[("Docs missing", "Misrouted")], drivers[("Docs missing", "Routed correctly")]
cm, clean = drivers[("Docs complete", "Misrouted")], drivers[("Docs complete", "Routed correctly")]
missing = mm["cases"] + mr["cases"]

data = {
    "ach": {
        "pareto": ach["02_return_code_pareto"],
        "segments": [r for r in ach["04_channel_by_validation"]
                     if r["debit_type"] == "First debit" and r["origination_channel"] in
                     ("Online Enrollment", "Mobile App", "Recurring Biller File", "Phone Agent")][:6],
        "sim": {"avoided_per_validation": (sim["returns_today"] - sim["returns_with_rule"]) / sim["entries_needing_validation"]},
    },
    "disputes": {
        "drivers": dsp["02_delay_drivers"],
        "forecast": dsp["forecast"],
        "sim": {
            "cases": dsp["cases"], "avg_days": dsp["scenario"]["avg_days_today"], "reopen": dsp["scenario"]["reopen_today"],
            "missing_cases": missing, "misrouted_cases": mm["cases"] + cm["cases"], "misrouted_only": cm["cases"],
            "avg_evidence_requests": (mm["avg_evidence_requests"] * mm["cases"] + mr["avg_evidence_requests"] * mr["cases"]) / missing,
            "coef_evidence": dsp["delay_model"]["evidence_requests"], "coef_misroute": dsp["delay_model"]["misrouted"],
            "reopen_missing": (mm["reopen_rate_pct"] * mm["cases"] + mr["reopen_rate_pct"] * mr["cases"]) / missing,
            "reopen_misrouted": cm["reopen_rate_pct"], "reopen_clean": clean["reopen_rate_pct"],
        },
    },
    "recon": recon,
    "denial": denial["denial_by_carc"],
    "funnel": funnel["funnel"],
    "ml": {"curve": ml["decision_curve"], "best": ml["best_contact"]},
    "ai": {k: v for k, v in ai.items() if k.endswith("_pct")},
    "invest": {"summary": inv["summary"], "policy": inv["01_drift_by_rebalance_policy"],
               "drift_points": inv["drift_points"], "risk_flags": inv["risk_flags"], "line": inv["book_vs_benchmark"]},
}
html = (HERE / "src/template.html").read_text().replace("__DATA__", json.dumps(data, separators=(",", ":")))
(HERE / "index.html").write_text(html)
print("wrote", HERE / "index.html", f"{len(html)/1024:.0f} KB")
