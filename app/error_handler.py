from flask import jsonify

def handle_key_error(e):
    return jsonify({'massege': 'KEY_ERROR', 'key': str(e), 'error': 400}), 400

def handle_validation_error(e):
    return jsonify({'massege': 'VALIDATION_ERROR', 'key': e.message, 'error': 400}), 400

def handle_login_error(e):
    if e.message == 'ID':
        return jsonify({'message': '등록되지 않은 유저입니다. 아이디를 확인해주세요', 'error': 404}), 404

    if e.message == 'PASSWORD':
        return jsonify({'message': '비밀번호가 일치하지 않습니다.', 'error': 405}), 405

    if e.message == 'REMOVED':
        return jsonify({'message': '이미 탈퇴한 유저입니다.', 'error': 406}), 406

    if e.message == 'DEACTIVATE':
        return jsonify({'message': '허가되지 않은 유저입니다.', 'error': 403}), 403
