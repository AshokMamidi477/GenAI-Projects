"""test_prompt_builder.py"""
import sys; sys.path.insert(0,"app")
from datetime import date, timedelta
from prompt_builder import calculate_weeks, build_study_plan_prompt

def test_12_weeks(): assert calculate_weeks(date.today()+timedelta(weeks=12))==12
def test_caps_at_52(): assert calculate_weeks(date.today()+timedelta(weeks=100))==52
def test_min_one(): assert calculate_weeks(date.today()+timedelta(days=3))>=1
def test_prompt_has_topic():
    p,_ = build_study_plan_prompt("Python","Beginner",10,date.today()+timedelta(weeks=8),[],"Get a job")
    assert "Python" in p
def test_prompt_has_week_count():
    p, weeks = build_study_plan_prompt("SQL","Beginner",5,date.today()+timedelta(weeks=6),[],"Learn SQL")
    assert str(weeks) in p
