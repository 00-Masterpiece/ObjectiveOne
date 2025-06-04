from flask import Blueprint, render_template, redirect, url_for, request, abort
from flask_login import login_required, current_user
from models import Goal, Completion, db
from forms import GoalForm
from datetime import date, timedelta, datetime
from utils import validate_time_interval, darken_hex
import calendar as cal_module

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    today = date.today()
    week = [today + timedelta(days=i) for i in range(7)]

    goals = Goal.query.filter_by(user_id=current_user.id).all()
    completions = Completion.query.with_entities(Completion.goal_id, Completion.date).all()
    completed_set = set((c.goal_id, c.date) for c in completions)

    calendar = {}
    daily_stats = {}

    for day in week:
        weekday_str = day.strftime('%a')
        weekday_name = day.strftime('%A')
        date_str = day.strftime('%Y-%m-%d')
        goals_for_day = []

        for goal in goals:
            if weekday_str in goal.days.split(','):
                done = (goal.id, day.strftime('%Y-%m-%d')) in completed_set
                goals_for_day.append((goal, done))
        
        calendar[(date_str, weekday_name)] = goals_for_day
        daily_stats[date_str] = {
            "completed": sum(1 for g, d in goals_for_day if d),
            "total": len(goals_for_day)
        }

        weekday_order = {day: i for i, day in enumerate(cal_module.day_name)}
        calendar = dict(sorted(calendar.items(), key=lambda x: weekday_order[x[0][1]]))

    return render_template('index.html', goals=goals, calendar=calendar, daily_stats=daily_stats, today=date.today().strftime('%Y-%m-%d'))


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_goal():
    form = GoalForm()
    if form.validate_on_submit():
        validate_time_interval(form)

        new_goal = Goal(
            user_id=current_user.id,
            name=form.name.data,
            days=",".join(form.days.data),
            color=form.color.data,
            badge_color=darken_hex(form.color.data),
            start_time=form.start_time.data.strftime("%H:%M") if form.start_time.data else None,
            end_time=form.end_time.data.strftime("%H:%M") if form.end_time.data else None
        )
        db.session.add(new_goal)
        db.session.commit()

        return redirect(url_for('main.index'))
    
    return render_template('add.html', form=form)


@main.route('/complete', methods=['POST'])
@login_required
def complete_goal():
    goal_id = int(request.form['goal_id'])
    day = request.form['date']

    existing = Completion.query.filter_by(user_id=current_user.id, goal_id=goal_id, date=day).first()

    if existing:
        db.session.delete(existing)  # ❌ Uncheck
        db.session.commit()
        return redirect(url_for('main.index'))  # No confetti
    else:
        completion = Completion(user_id=current_user.id, goal_id=goal_id, date=day)
        db.session.add(completion)  # ✅ Check
        db.session.commit()
        return redirect(url_for('main.index') + "?completed=true")  # Confetti



@main.route('/edit/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def edit_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        abort(403)

    form = GoalForm(obj=goal)

    if form.validate_on_submit():
        validate_time_interval(form)
        
        goal.user_id=current_user.id
        goal.name = form.name.data
        goal.days = ",".join(form.days.data) if isinstance(form.days.data, list) else form.days.data

        # Parse time from string input (from JS picker or HTML input)
        if isinstance(form.start_time.data, str):
            goal.start_time = datetime.strptime(form.start_time.data, "%H:%M").strftime("%H:%M")
        else:
            if goal.start_time:
                goal.start_time = form.start_time.data.strftime("%H:%M")

        if isinstance(form.end_time.data, str):
            goal.end_time = datetime.strptime(form.end_time.data, "%H:%M").strftime("%H:%M")
        else:
            if goal.end_time:
                goal.end_time = form.end_time.data.strftime("%H:%M")

        goal.color = form.color.data
        goal.badge_color=darken_hex(form.color.data)

        db.session.commit()

        return redirect(url_for('main.index'))


    # Pre-fill checkboxes and time correctly
    form.days.data = goal.days.split(',')
    if goal.start_time:
        form.start_time.data = datetime.strptime(goal.start_time, "%H:%M").time()
    if goal.end_time:
        form.end_time.data = datetime.strptime(goal.end_time, "%H:%M").time()

    return render_template('edit.html', form=form, goal=goal)


@main.route('/delete/<int:goal_id>', methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        abort(403)
    
    Completion.query.filter_by(goal_id=goal.id).delete()
    db.session.delete(goal)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/profile')
@login_required
def profile():
    total_goals = Goal.query.filter_by(user_id=current_user.id).count()
    completed = Completion.query.filter_by(user_id=current_user.id).count()

    return render_template('profile.html', total=total_goals, completed=completed)


