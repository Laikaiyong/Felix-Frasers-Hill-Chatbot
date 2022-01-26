from app.views import blueprint
from flask import render_template

PLANS = [
    {
        "name":"Plan A",
        "time":[
            "8:00a.m. - 8:30p.m.",
            "8:30a.m. - 10:30a.m.",
            "10:30a.m. - 12:30a.m.",
            "12:30a.m. - 1:00p.m.",
            "1:00p.m.- 2:00p.m.",
            "2:00p.m.- 3:00p.m.",
            "3:00p.m. - 5:30p.m.",
            "5:30p.m.- 6:30p.m.",
            "6:30p.m - 7:30p.m."
        ],
        "activity":[
            "Relax at Jeriau Waterfall.",
            "Hike at Bishop's Trail",
            "Go for birdwatching.",
            "Hike at Hemmant Trail.",
            "Have a lunch Arzed Cafe.",
            "Visit the Clock Tower.",
            "Playing golf at Fraser's Hill Golf Club.",
            "Shopping souvenirs at Kraftangan & Cenderamata Bukit Fraser.",
            "Dinner at The Hillview Restaurant."
        ]
    },
    {
        "name":"Plan B",
        "time":[
            "8:00a.m. - 8:30p.m.",
            "8:30a.m. - 9:30a.m.",
            "9:30a.m. - 11:30a.m.",
            "11:30a.m. - 1:00p.m.",
            "1:00p.m.- 2:00p.m.",
            "2:00p.m.- 3:30p.m.",
            "3:30p.m. - 5:30p.m.",
            "5:30p.m.- 6:30p.m.",
            "6:30p.m - 7:30p.m."
        ],
        "activity":[
            "Visit clock tower and snapshots.",
            "Go for birdwatching.",
            "Hike at one of the trails (Pine Tree trail not recommended).",
            "Head over to The Paddocks for archery and horse rides.",
            "Lunch at Scott's Restaurant and Pub.",
            "Chill at Jeriau Waterfall.",
            "Enjoy water sports at Allen's water",
            "Visit Sanyi's Orchid Garden.",
            "Dinner at The Olde Smokehouse.."
        ]
    }
]

# http://127.0.0.1:5000/plan
@blueprint.route('/plan')
def plan_a():
    return render_template(
                'plan.html', 
                plans=PLANS
            )