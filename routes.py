from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Submission, Feedback
from diagnostic_engine import DiagnosticEngine
import json

# Initialize diagnostic engine
diagnostic_engine = DiagnosticEngine()

@app.route('/')
def index():
    """Main page with symptom input form"""
    symptoms = diagnostic_engine.get_all_symptoms()
    example_bundles = diagnostic_engine.get_example_symptom_bundles()
    return render_template('index.html', symptoms=symptoms, example_bundles=example_bundles)

@app.route('/diagnose', methods=['POST'])
def diagnose():
    """Process symptoms and provide diagnosis"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        age = request.form.get('age')
        gender = request.form.get('gender')
        location = request.form.get('location', '').strip()
        
        # Get symptoms
        selected_symptoms = request.form.getlist('symptoms')
        symptoms_text = request.form.get('symptoms_text', '').strip()
        
        # Validate that at least some symptoms are provided
        if not selected_symptoms and not symptoms_text:
            flash('Please select symptoms or describe how you feel.', 'error')
            return redirect(url_for('index'))
        
        # Process age
        age_int = None
        if age and age.strip():
            try:
                age_int = int(age)
                if age_int < 0 or age_int > 150:
                    age_int = None
            except ValueError:
                age_int = None
        
        # Get diagnosis from engine
        diagnosis_result = diagnostic_engine.diagnose(selected_symptoms, symptoms_text)
        
        # Save to database
        submission = Submission(
            name=name if name else None,
            age=age_int,
            gender=gender if gender else None,
            location=location if location else None,
            symptoms_selected=selected_symptoms,
            symptoms_text=symptoms_text if symptoms_text else None,
            diagnosis=diagnosis_result
        )
        
        db.session.add(submission)
        db.session.commit()
        
        return render_template('diagnosis.html', 
                             diagnosis=diagnosis_result, 
                             submission=submission)
    
    except Exception as e:
        app.logger.error(f"Error in diagnosis: {str(e)}")
        flash('An error occurred while processing your symptoms. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/feedback/<int:submission_id>', methods=['GET', 'POST'])
def feedback(submission_id):
    """Handle feedback submission"""
    submission = Submission.query.get_or_404(submission_id)
    
    if request.method == 'POST':
        try:
            is_accurate = request.form.get('is_accurate') == 'yes'
            comments = request.form.get('comments', '').strip()
            
            # Check if feedback already exists
            existing_feedback = Feedback.query.filter_by(submission_id=submission_id).first()
            
            if existing_feedback:
                # Update existing feedback
                existing_feedback.is_accurate = is_accurate
                existing_feedback.comments = comments if comments else None
            else:
                # Create new feedback
                feedback_obj = Feedback(
                    submission_id=submission_id,
                    is_accurate=is_accurate,
                    comments=comments if comments else None
                )
                db.session.add(feedback_obj)
            
            db.session.commit()
            flash('Thank you for your feedback! It helps us improve our diagnostic accuracy.', 'success')
            return redirect(url_for('history'))
            
        except Exception as e:
            app.logger.error(f"Error saving feedback: {str(e)}")
            flash('An error occurred while saving your feedback. Please try again.', 'error')
    
    return render_template('feedback.html', submission=submission)

@app.route('/history')
def history():
    """Display user submission history"""
    try:
        # Get all submissions ordered by most recent first
        submissions = Submission.query.order_by(Submission.created_at.desc()).all()
        return render_template('history.html', submissions=submissions)
    
    except Exception as e:
        app.logger.error(f"Error loading history: {str(e)}")
        flash('An error occurred while loading the history.', 'error')
        return render_template('history.html', submissions=[])

@app.route('/api/example-symptoms/<bundle_name>')
def get_example_symptoms(bundle_name):
    """API endpoint to get example symptoms for a bundle"""
    try:
        bundles = diagnostic_engine.get_example_symptom_bundles()
        bundle = next((b for b in bundles if b['name'].lower().replace(' ', '-') == bundle_name.lower()), None)
        
        if bundle:
            return jsonify({'symptoms': bundle['symptoms']})
        else:
            return jsonify({'error': 'Bundle not found'}), 404
            
    except Exception as e:
        app.logger.error(f"Error getting example symptoms: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', 
                         page_title='Page Not Found',
                         content='<div class="text-center"><h2 class="text-2xl font-bold text-gray-800 mb-4">Page Not Found</h2><p class="text-gray-600">The page you are looking for does not exist.</p><a href="/" class="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Go Home</a></div>'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html',
                         page_title='Internal Error', 
                         content='<div class="text-center"><h2 class="text-2xl font-bold text-gray-800 mb-4">Internal Server Error</h2><p class="text-gray-600">An unexpected error occurred. Please try again later.</p><a href="/" class="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Go Home</a></div>'), 500
