from flask import Blueprint, render_template, request, redirect, url_for

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    return render_template('dashboard.html')


@main_bp.route('/upload', methods=['GET', 'POST'])
def upload_dataset():
    if request.method == 'POST':
        # placeholder for handling uploads
        return redirect(url_for('main.dashboard'))
    return render_template('upload_dataset.html')


@main_bp.route('/results')
def results():
    return render_template('results.html')
