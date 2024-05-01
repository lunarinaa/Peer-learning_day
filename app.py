from flask import Flask, jsonify, request

app = Flask(__name__)

admins = []
users = []
companies = []
problems = []

admins = [
    {
        "id": 1,
        "username": "admin1",
        "email": "admin1@example.com",
        "password": "adminpass1"
    },
    {
        "id": 2,
        "username": "admin2",
        "email": "admin2@example.com",
        "password": "adminpass2"
    }
]

users = [
    {
        "id": 1,
        "username": "user1",
        "email": "user1@example.com",
        "password": "userpass1"
    },
    {
        "id": 2,
        "username": "user2",
        "email": "user2@example.com",
        "password": "userpass2"
    }
]
companies = [
    {
        "id": 1,
        "name": "Company A",
        "email": "companyA@example.com",
        "password": "password123",
        "approved": False
    },
    {
        "id": 2,
        "name": "Company B",
        "email": "companyB@example.com",
        "password": "password456",
        "approved": True
    }
]

problems = [
    {
        "id": 1,
        "description": "Issue with product delivery",
        "reported_by": "user@example.com",
        "resolved": False
    },
    {
        "id": 2,
        "description": "Payment gateway not working",
        "reported_by": "companyB@example.com",
        "resolved": False
    }
]

@app.route('/api/companies/pending', methods=['GET'])
def list_pending_companies():
    pending_companies = [company for company in companies if not company['approved']]
    return jsonify(pending_companies), 200

@app.route('/api/companies/<int:company_id>/approve', methods=['POST'])
def approve_company(company_id):
    for company in companies:
        if company['id'] == company_id:
            company['approved'] = True
            return jsonify({'message': 'Company approved'}), 200
    return jsonify({'message': 'Company not found'}), 404

@app.route('/api/companies/<int:company_id>/reject', methods=['POST'])
def reject_company(company_id):
    for company in companies:
        if company['id'] == company_id:
            company['approved'] = False
            return jsonify({'message': 'Company rejected'}), 200
    return jsonify({'message': 'Company not found'}), 404

@app.route('/api/admins', methods=['POST'])
def create_admin():
    new_admin = request.json
    admins.append(new_admin)
    return jsonify(new_admin), 201

@app.route('/api/admins', methods=['GET'])
def list_admins():
    return jsonify(admins), 200

@app.route('/api/users/register', methods=['POST'])
def register_user():
    new_user = request.json
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/api/companies/register', methods=['POST'])
def register_company():
    new_company = request.json
    companies.append(new_company)
    return jsonify(new_company), 201

@app.route('/api/users/login', methods=['POST'])
def login_user():
    credentials = request.json
    user = next((user for user in users if user['email'] == credentials['email']), None)
    if user and user['password'] == credentials['password']:
        return jsonify({'message': 'User logged in'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/companies/login', methods=['POST'])
def login_company():
    credentials = request.json
    company = next((company for company in companies if company['email'] == credentials['email']), None)
    if company and company['password'] == credentials['password']:
        return jsonify({'message': 'Company logged in'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/problems', methods=['POST'])
def submit_problem():
    new_problem = request.json
    problems.append(new_problem)
    return jsonify(new_problem), 201

@app.route('/api/problems', methods=['GET'])
def list_problems():
    return jsonify(problems), 200

@app.route('/api/problems/reviews', methods=['GET'])
def view_problems_for_review():
    return jsonify(problems), 200

@app.route('/api/problems/<int:problem_id>/resolve', methods=['POST'])
def resolve_problem(problem_id):
    problem = next((problem for problem in problems if problem['id'] == problem_id), None)
    if problem:
        problem['resolved'] = True
        return jsonify({'message': 'Problem resolved'}), 200
    return jsonify({'message': 'Problem not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100)
