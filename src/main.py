# src/main.py

import os
from typing import Dict, Any

from .utils import (
    load_facebook_data,
    build_data_summary,
    save_json,
    append_log,
)
from .agents import (
    run_planner,
    run_data_agent,
    run_insight_agent,
    run_evaluator_agent,
    run_creative_agent,
    build_evaluation_stats,
    build_creative_context,
)


DATA_PATH = os.getenv("FB_DATA_PATH", "data/facebook_ads.csv")
OUTPUT_DIR = "outputs"
INSIGHTS_PATH = os.path.join(OUTPUT_DIR, "insights.json")
CREATIVES_PATH = os.path.join(OUTPUT_DIR, "creatives.json")
LOG_PATH = os.path.join(OUTPUT_DIR, "logs.txt")


def run_pipeline(user_question: str) -> Dict[str, Any]:
    append_log(LOG_PATH, f"=== New run ===")
    append_log(LOG_PATH, f"Question: {user_question}")

    # 1. Load data
    df = load_facebook_data(DATA_PATH)
    append_log(LOG_PATH, f"Loaded dataframe with {len(df)} rows.")

    # 2. Planner Agent
    plan = run_planner(user_question)
    append_log(LOG_PATH, f"Planner output: {plan}")

    # 3. Build numeric summary (system code)
    data_summary = build_data_summary(df)
    append_log(LOG_PATH, "Built numeric data summary.")

    # 4. Data Agent (LLM summary)
    data_agent_view = run_data_agent(data_summary)
    append_log(LOG_PATH, f"Data Agent view: {data_agent_view}")

    # 5. Insight Agent (hypotheses)
    insights = run_insight_agent(user_question, data_summary, data_agent_view)
    append_log(LOG_PATH, f"Insight Agent output: {insights}")

    # 6. Evaluator Agent
    eval_stats = build_evaluation_stats(data_summary)
    evaluations = run_evaluator_agent(insights, eval_stats)
    append_log(LOG_PATH, f"Evaluator Agent output: {evaluations}")

    # 7. Creative Agent
    creative_context = build_creative_context(data_summary)
    creatives = run_creative_agent(creative_context)
    append_log(LOG_PATH, f"Creative Agent output: {creatives}")

    # 8. Save outputs
    insights_output = {
        "question": user_question,
        "plan": plan,
        "data_summary": data_summary,
        "data_agent_view": data_agent_view,
        "insights": insights,
        "evaluations": evaluations,
    }
    save_json(INSIGHTS_PATH, insights_output)
    save_json(CREATIVES_PATH, creatives)

    append_log(LOG_PATH, "Saved insights.json and creatives.json")
    return {
        "insights": insights_output,
        "creatives": creatives,
    }


if __name__ == "__main__":
    # You can change this default question or accept input from CLI.
    default_question = (
        "Diagnose why ROAS has changed over the last 30 days and "
        "recommend new creative ideas for low-CTR campaigns."
    )
    result = run_pipeline(default_question)
    print("Run complete.")
    print(f"Insights saved to: {INSIGHTS_PATH}")
    print(f"Creatives saved to: {CREATIVES_PATH}")
