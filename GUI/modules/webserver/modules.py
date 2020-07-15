from flask import Blueprint, render_template

bp_modules = Blueprint('modules', __name__)


@bp_modules.route('/games')
def games():
    return render_template('games.html', currentSite='games')


@bp_modules.route('/settings')
def settings():
    return render_template('settings.html', currentSite='settings')
