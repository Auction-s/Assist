# src/prioritize.py
"""
Priority scoring utilities for Smart Task Assistant.

Functions:
- days_until(d, ref) -> float days or None
- urgency_score(days) -> 0..1 (piecewise)
- importance_score(imp) -> 0..1 (map 2/1/0/None)
- time_score(est_minutes) -> 0..1 (shorter tasks get higher score)
- score_task(task, ref=None, weights=(0.6,0.3,0.1)) -> priority 0..1
- rank_tasks(tasks, ref=None, weights=(...)) -> list of (score, task) sorted desc

Expected input `task` is a dict with keys produced by `parse_task()`:
{
  'raw': str,
  'title': str,
  'due': datetime or None,
  'est_minutes': int or None,
  'importance': 2|1|0|None
}
"""

from datetime import datetime
import math

def days_until(d, ref=None):
    """Return days (float) from ref until datetime d. If d is None return None."""
    if d is None:
        return None
    ref = ref or datetime.now()
    delta = d - ref
    return delta.total_seconds() / (3600.0 * 24.0)

def urgency_score(days):
    """
    Piecewise urgency mapping -> 0..1 (1 = most urgent).
    - days <= 0   : 1.0 (due now or overdue)
    - 0 < days < 1: 0.95
    - 1 <= days < 3: 0.8
    - 3 <= days < 7: 0.6
    - 7 <= days < 30: 0.3
    - >=30: 0.05  (very low urgency)
    - None (no due date): 0.0 (not urgent)
    """
    if days is None:
        return 0.0
    if days <= 0:
        return 1.0
    if days < 1:
        return 0.95
    if days < 3:
        return 0.80
    if days < 7:
        return 0.60
    if days < 30:
        return 0.30
    return 0.05

def importance_score(imp):
    """
    Map importance (0=high,1=medium,-1=low,None) to 0..1.
    Default None -> 0.5 (neutral)
    """
    if imp is None:
        return 0.5
    mapping = {0: 1, 1: 0.5, 2: 0.1}
    return mapping.get(imp, 0.5)

def time_score(est_minutes):
    """
    Map estimated time to 0..1 where smaller tasks score higher (prefer short wins).
    - None (unknown) -> 0.5 neutral
    - <=15m -> 1.0
    - <=60m -> 0.8
    - <=180m -> 0.5
    - >180m -> 0.2
    """
    if est_minutes is None:
        return 0.5
    try:
        m = float(est_minutes)
    except Exception:
        return 0.5
    if m <= 15:
        return 1.0
    if m <= 60:
        return 0.8
    if m <= 180:
        return 0.5
    return 0.2

def score_task(task, ref=None, weights=(0.6, 0.3, 0.1)):
    """
    Compute priority score in 0..1 for a parsed task dict.

    Final raw score = urgency*W_urg + importance*W_imp + time_score*W_time
    Return normalized score in 0..1 by dividing by sum(weights) (so final in 0..1).
    """
    # Defensive: accept either dict or None
    if task is None:
        return 0.0

    # Compute components
    due = task.get('due')
    days = None
    if due is not None:
        try:
            days = days_until(due, ref)
        except Exception:
            days = None

    u = urgency_score(days)
    imp = importance_score(task.get('importance'))
    t = time_score(task.get('est_minutes'))

    w_urg, w_imp, w_time = weights
    raw = (u * w_urg) + (imp * w_imp) + (t * w_time)

    # Normalize by sum of weights to keep result within 0..1
    denom = float(w_urg + w_imp + w_time) if (w_urg + w_imp + w_time) != 0 else 1.0
    score = raw / denom

    # small numeric safety clamp
    return max(0.0, min(1.0, float(score)))

def rank_tasks(tasks, ref=None, weights=(0.6,0.3,0.1)):
    """
    Given an iterable of task dicts (parsed tasks), return list of tuples:
    [(score, task_dict), ...] sorted descending by score.
    """
    scored = []
    for t in tasks:
        s = score_task(t, ref=ref, weights=weights)
        scored.append((s, t))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored

# ---------------- Demo when run as script ----------------
if __name__ == "__main__":
    # Quick demo using sample parsed-like objects (if you have parser.py,
    # you can import parse_task and build tasks from free text.)
    from datetime import timedelta
    now = datetime.now()

    demo_tasks = [
        # due tomorrow, high importance, 120 min
        {'raw':'Finish slides for meeting next Tue, ~2h, high importance',
         'title':'Finish slides','due': now + timedelta(days=1),'est_minutes':120,'importance':2},
        # no due date, medium importance, 30 min
        {'raw':'Refactor logging, 30min','title':'Refactor logging','due': None,'est_minutes':30,'importance':1},
        # due in 10 days, low importance, 240 min
        {'raw':'Work on side project','title':'Side project','due': now + timedelta(days=10),'est_minutes':240,'importance':0},
        # overdue item
        {'raw':'Submit tax form','title':'Submit tax','due': now - timedelta(days=1),'est_minutes':30,'importance':2},
        # quick micro task, no due
        {'raw':'Quick email to Sarah','title':'Email Sarah','due': None,'est_minutes':10,'importance':None},
    ]

    ranked = rank_tasks(demo_tasks, ref=now)
    print("Ranked tasks (score, title):")
    for score, t in ranked:
        print(f"{score:.3f}  — {t['title']}  (due={t['due']}, est={t['est_minutes']}, imp={t['importance']})")
