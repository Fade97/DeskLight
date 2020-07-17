from flask import Blueprint, render_template, request, redirect

bp_modules = Blueprint('modules', __name__)


@bp_modules.route('/games')
def games():
    return render_template('games.html', currentSite='games')


@bp_modules.route('/settings')
def settings():
    return render_template('settings.html', currentSite='settings')


@bp_modules.route('/updateleds', methods=['GET', 'POST'])
def updateleds():
    if request.method == "POST":
        req = request.form
        print(req.get('command'))
        from webserver import inBuffer
        inBuffer('<1,' + req.get('sliderR') + ',' +
                 req.get('sliderG') + ',' + req.get('sliderB') + '>')
        return redirect('/settings')
