import rules


@rules.predicate
def can_delete_user_social_auth(user, user_social_auth):
    return user_social_auth.allowed_to_disconnect(user, user_social_auth.provider)

rules.add_rule('can_delete_user_social_auth', can_delete_user_social_auth)
