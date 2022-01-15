from apu_cas import require_service_ticket, get_user_cas_attributes

from flask import Blueprint, render_template, jsonify

blueprint = Blueprint('views', __name__)

# Route Declaration
from app.views import chatbot

@blueprint.route('/')
@require_service_ticket
def index():
    user_attribute = get_user_cas_attributes()
    return jsonify({
        'is_from_new_login': user_attribute.is_from_new_login[0],
        'mail': user_attribute.mail[0],
        'authentication_date': user_attribute.authentication_date[0],
        'sam_account_name': user_attribute.sam_account_name[0],
        'display_name': user_attribute.display_name[0],
        'cn': user_attribute.cn[0],
        'title': user_attribute.title or None,
        'saml_authentication_statement_auth_method': user_attribute.saml_authentication_statement_auth_method[0],
        'credential_type': user_attribute.credential_type[0],
        'authentication_method': user_attribute.authentication_method[0],
        'long_term_authentication_request_token_used': user_attribute.long_term_authentication_request_token_used[0],
        'member_of': user_attribute.member_of or None,
        'department': user_attribute.department,
        'user_principal_name': user_attribute.user_principal_name[0]
    })