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
        from webserver import inBuffer
        inBuffer('<1,' + str(int(float(req.get('colorR')))) + ',' +
                 str(int(float(req.get('colorG')))) + ',' + str(int(float(req.get('colorB')))) + '>')
        return redirect('/settings')
