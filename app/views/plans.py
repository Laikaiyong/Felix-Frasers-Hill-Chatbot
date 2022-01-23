from app.views import blueprint
from flask import render_template

# http://127.0.0.1:5000/plan
@blueprint.route('/plan')
def plan_a():
    return render_template('plan.html')