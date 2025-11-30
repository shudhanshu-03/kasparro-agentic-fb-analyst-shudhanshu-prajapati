# src/agents.py

from typing import Any, Dict, List

from .prompts import (
    PLANNER_PROMPT,
    DATA_AGENT_PROMPT,
    INSIGHT_AGENT_PROMPT,
    EVALUATOR_AGENT_PROMPT,
    CREATIVE_AGENT_PROMPT,
)
from .utils import call_llm, safe_json_loads, build_data_summary


def run_planner(user_question: str) -> Dict[str, Any]:
    user_prompt = f"User question:\n\"\"\"{user_question}\"\"\"\n\nProduce the plan JSON."
    raw = call_llm(PLANNER_PROMPT, user_prompt)
    return safe_json_loads(raw)


def run_data_agent(summary_stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    Here the 'system code' has already computed summary_stats (build_data_summary).
    We send that to the LLM so it can express a human-readable summary.
    """
    user_prompt = (
        "You are given compact performance statistics as JSON.\n"
        "Use them to summarize what is happening in the account.\n\n"
        f"DATA SUMMARY (JSON):\n```json\n{summary_stats}\n```"
    )
    raw = call_llm(DATA_AGENT_PROMPT, user_prompt)
    return safe_json_loads(raw)


def run_insight_agent(user_question: str,
                      data_summary: Dict[str, Any],
                      data_agent_view: Dict[str, Any]) -> Dict[str, Any]:
    user_prompt = (
        f"User question:\n\"\"\"{user_question}\"\"\"\n\n"
        "System numeric summary:\n"
        f"```json\n{data_summary}\n```\n\n"
        "Data Agent textual summary:\n"
        f"```json\n{data_agent_view}\n```"
    )
    raw = call_llm(INSIGHT_AGENT_PROMPT, user_prompt)
    return safe_json_loads(raw)


def run_evaluator_agent(insights: Dict[str, Any],
                        evaluation_stats: Dict[str, Any]) -> Dict[str, Any]:
    """
    evaluation_stats can be derived from data_summary (e.g. deltas, top movers).
    For simplicity here we just pass the same summary structure again.
    """
    user_prompt = (
        "You are given hypotheses and quantitative stats.\n\n"
        f"HYPOTHESES JSON:\n```json\n{insights}\n```\n\n"
        f"QUANTITATIVE STATS JSON:\n```json\n{evaluation_stats}\n```"
    )
    raw = call_llm(EVALUATOR_AGENT_PROMPT, user_prompt)
    return safe_json_loads(raw)


def run_creative_agent(creative_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    creative_context should contain low_ctr_campaigns and high_ctr_creatives.
    """
    user_prompt = (
        "You are given context for low-CTR and high-CTR creatives as JSON.\n"
        "Propose new creatives following the output schema.\n\n"
        f"CREATIVE CONTEXT JSON:\n```json\n{creative_context}\n```"
    )
    raw = call_llm(CREATIVE_AGENT_PROMPT, user_prompt)
    return safe_json_loads(raw)


def build_evaluation_stats(data_summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Optionally compute extra numbers; currently just passes through.
    You can expand this with deltas, comparisons etc.
    """
    # For now we just forward the whole summary and mark where ROAS seems to drop.
    eval_stats: Dict[str, Any] = {"base_summary": data_summary}

    roas_by_date = data_summary.get("roas_by_date", [])
    if len(roas_by_date) >= 2:
        first = roas_by_date[0]
        last = roas_by_date[-1]
        start_roas = first.get("roas", 0.0)
        end_roas = last.get("roas", 0.0)
        delta = end_roas - start_roas
        pct_change = (delta / start_roas * 100.0) if start_roas != 0 else 0.0
        eval_stats["roas_trend"] = {
            "start_date": first.get("date"),
            "start_roas": start_roas,
            "end_date": last.get("date"),
            "end_roas": end_roas,
            "absolute_change": delta,
            "pct_change": pct_change,
        }

    eval_stats["note"] = "You can use roas_trend and campaign summaries to judge hypotheses."
    return eval_stats


def build_creative_context(data_summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "low_ctr_campaigns": data_summary.get("low_ctr_campaigns", []),
        "high_ctr_creatives": data_summary.get("high_ctr_creatives", []),
    }
