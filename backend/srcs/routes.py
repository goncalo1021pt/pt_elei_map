from flask import Blueprint, jsonify, request
from src.models import db, Election, DicoCode, Result
from sqlalchemy import func

api = Blueprint('api', __name__, url_prefix='/api')


def register_routes(app):
    """Register all blueprints"""
    app.register_blueprint(api)

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'ok'}), 200


# Elections endpoints
@api.route('/elections', methods=['GET'])
def list_elections():
    """Get all elections"""
    elections = Election.query.all()
    return jsonify([e.to_dict() for e in elections]), 200


@api.route('/elections/<election_id>', methods=['GET'])
def get_election(election_id):
    """Get election details"""
    election = Election.query.filter_by(election_id=election_id).first()
    if not election:
        return jsonify({'error': 'Election not found'}), 404
    return jsonify(election.to_dict()), 200


# DICO codes endpoints
@api.route('/dico', methods=['GET'])
def list_dico():
    """Get DICO codes, optionally filtered by level or parent"""
    level = request.args.get('level', type=int)
    parent = request.args.get('parent')

    query = DicoCode.query

    if level:
        query = query.filter_by(level=level)
    if parent:
        query = query.filter_by(parent_code=parent)

    codes = query.all()
    return jsonify([c.to_dict() for c in codes]), 200


@api.route('/dico/<code>', methods=['GET'])
def get_dico(code):
    """Get DICO code details"""
    dico = DicoCode.query.filter_by(code=code).first()
    if not dico:
        return jsonify({'error': 'DICO code not found'}), 404
    
    result = dico.to_dict()
    result['children'] = [c.to_dict() for c in dico.children]
    return jsonify(result), 200


# Results endpoints
@api.route('/results/<election_id>', methods=['GET'])
def get_results_by_election(election_id):
    """Get results for an election, optionally filtered by geography level"""
    level = request.args.get('level', type=int)

    query = Result.query.filter_by(election_id=election_id)

    if level:
        # Join with DicoCode to filter by level
        query = query.join(DicoCode).filter(DicoCode.level == level)

    results = query.all()
    return jsonify([r.to_dict() for r in results]), 200


@api.route('/results/<election_id>/<dico_code>', methods=['GET'])
def get_results_by_geography(election_id, dico_code):
    """Get results for specific geography in an election"""
    results = Result.query.filter_by(
        election_id=election_id,
        dico_code=dico_code
    ).all()

    if not results:
        return jsonify({'error': 'No results found'}), 404

    return jsonify([r.to_dict() for r in results]), 200


@api.route('/results/<election_id>/<dico_code>/summary', methods=['GET'])
def get_results_summary(election_id, dico_code):
    """Get aggregated results summary for a geography"""
    results = Result.query.filter_by(
        election_id=election_id,
        dico_code=dico_code
    ).all()

    if not results:
        return jsonify({'error': 'No results found'}), 404

    total_votes = sum(r.votes for r in results)
    summary = [
        {
            'party_code': r.party_code,
            'votes': r.votes,
            'percentage': float(r.percentage) if r.percentage else round((r.votes / total_votes * 100), 2) if total_votes > 0 else 0
        }
        for r in sorted(results, key=lambda x: x.votes, reverse=True)
    ]

    return jsonify({
        'election_id': election_id,
        'dico_code': dico_code,
        'total_votes': total_votes,
        'results': summary
    }), 200


# Statistics endpoints
@api.route('/stats/<election_id>', methods=['GET'])
def get_election_stats(election_id):
    """Get statistics for an election"""
    election = Election.query.filter_by(election_id=election_id).first()
    if not election:
        return jsonify({'error': 'Election not found'}), 404

    results = Result.query.filter_by(election_id=election_id).all()
    total_votes = sum(r.votes for r in results)
    total_results = len(results)
    unique_parties = len(set(r.party_code for r in results))
    unique_locations = len(set(r.dico_code for r in results))

    return jsonify({
        'election_id': election_id,
        'name': election.name,
        'total_votes': total_votes,
        'total_results': total_results,
        'unique_parties': unique_parties,
        'unique_locations': unique_locations
    }), 200
