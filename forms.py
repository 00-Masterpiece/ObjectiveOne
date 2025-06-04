from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TimeField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import ColorInput, CheckboxInput, ListWidget

class GoalForm(FlaskForm):
    name = StringField('Goal Name', validators=[DataRequired()])
    days = SelectMultipleField(
        'Days',
        choices=[('Mon', 'Mon'), ('Tue', 'Tue'), ('Wed', 'Wed'), 
                 ('Thu', 'Thu'), ('Fri', 'Fri'), ('Sat', 'Sat'), ('Sun', 'Sun')],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )
    start_time = TimeField('Start Time (optional)', format='%H:%M', render_kw={"placeholder": "HH:MM"}, default=None, validators=[Optional()])
    end_time = TimeField('End Time (optional)', format='%H:%M', render_kw={"placeholder": "HH:MM"}, default=None, validators=[Optional()])
    color = StringField('Color', widget=ColorInput(), default='#44aaff')
