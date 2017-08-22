from social_core.backends.gitlab import GitLabOAuth2


class ShackGitLabOAuth2(GitLabOAuth2):
    name = 'shackgitlab'
    API_URL = 'https://git.shackspace.de'
    AUTHORIZATION_URL = 'https://git.shackspace.de/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://git.shackspace.de/oauth/token'
