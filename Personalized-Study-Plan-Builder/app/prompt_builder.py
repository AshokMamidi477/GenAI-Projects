"""prompt_builder.py — Week calculation and prompt construction"""
from datetime import date

MAX_WEEKS = 52

def calculate_weeks(target_date):
    return max(1, min((target_date - date.today()).days // 7, MAX_WEEKS))

def build_study_plan_prompt(topic, level, hours_per_week, target_date, resources, goal):
    weeks = calculate_weeks(target_date)
    resources_str = ", ".join(resources) if resources else "any format"
    prompt = f"""You are an expert curriculum designer. Design a personalised week-by-week study plan.

LEARNER PROFILE:
- Topic: {topic}
- Current level: {level}
- Available time: {hours_per_week} hours per week
- Duration: {weeks} weeks (target: {target_date})
- Goal: {goal}
- Preferred resources: {resources_str}

FORMAT — use this Markdown structure for EVERY week:
## Week N: [Theme]
### Learning Objectives
- [3 bullet points]
### Resources
- [2-3 matched to their preferred types]
### Practice Exercise
[One concrete task]
### Checkpoint
[One question to test understanding]

After all weeks, add:
## Key Milestones
- Week {max(1,weeks//4)}: 25% checkpoint
- Week {max(1,weeks//2)}: 50% checkpoint
- Week {max(1,3*weeks//4)}: 75% checkpoint
- Week {weeks}: Completion

RULES: Write all {weeks} weeks. Be realistic. Match resources to: {resources_str}."""
    return prompt, weeks
