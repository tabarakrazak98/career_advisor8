from flask import Flask, render_template, request, abort, url_for
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import os
import json

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
csrf = CSRFProtect(app)

# Load courses data
try:
    with open('data/courses.json', 'r', encoding='utf-8') as f:
        courses_data = json.load(f)
except FileNotFoundError:
    print("Error: courses.json file not found in data/ directory")
    courses_data = []

# Configuration
VALID_FIELDS = {course['field'] for course in courses_data}
VALID_LEVELS = {'beginner', 'professional'}
VALID_COURSE_TYPES = {'مجاني', 'مدفوع', 'كلاهما'}

CAREER_SUGGESTIONS = {
    'برمجة': 'مطور برامج أو تطبيقات ويب',
    'تحليل البيانات': 'محلل بيانات أو محلل أعمال',
    'تصميم': 'مصمم واجهات أو مصمم جرافيك',
    'تسويق': 'خبير تسويق رقمي أو مدير حملات',
    'ذكاء اصطناعي': 'باحث في الذكاء الاصطناعي أو مهندس تعلم آلي'
}

@app.route('/')
def home():
    """Render home page with courses and search form"""
    return render_template(
        'index.html',
        fields=sorted(VALID_FIELDS),
        all_courses=courses_data,
        current_year=datetime.now().year
    )

@app.route('/results', methods=['POST'])
def handle_results():
    """Process form submission and display results"""
    try:
        # CSRF Protection
        if not request.form.get('csrf_token'):
            abort(400, "Invalid request: CSRF token missing")
            
        # Get form data
        field = request.form.get('skills_interests', '').strip()
        level = request.form.get('level', '').strip()
        course_type = request.form.get('course_type', '').strip()

        # Validate inputs
        if not field or field not in VALID_FIELDS:
            abort(400, "Invalid field selected")
            
        if level not in VALID_LEVELS:
            abort(400, "Invalid skill level")
            
        if course_type not in VALID_COURSE_TYPES:
            abort(400, "Invalid course type")

        # Filter courses
        filtered_courses = [
            course for course in courses_data
            if course['field'] == field
            and course['level'] == level
            and (course['type'] == course_type or course_type == 'كلاهما')
        ]

        # Prepare context
        context = {
            'selected_field': field,
            'user_level': 'مبتدئ' if level == 'beginner' else 'محترف',
            'course_type': course_type,
            'courses': filtered_courses,
            'courses_count': len(filtered_courses),
            'career': CAREER_SUGGESTIONS.get(field, 'مجال مهني عام'),
            'current_date': datetime.now().strftime("%Y-%m-%d"),
            'current_year': datetime.now().year
        }

        return render_template('results.html', **context)

    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        abort(500)

# Error Handlers
@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html', error=error.description), 400

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', error=error.description), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', error=error.description), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)