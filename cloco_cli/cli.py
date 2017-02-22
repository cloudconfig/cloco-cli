import click
import configparser
import json
import os
import requests
import sys
from requests.auth import HTTPBasicAuth


@click.group()
def main():
    """A command line interface for the cloco API."""
    return


@main.command()
@click.option('--key', help='The client key', default='')
@click.option('--secret', help='The client secret', default='')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--env', help='The environment identifier, if not supplied will use the environment stored in preferences', default='')
@click.option('--url', help='The cloco url', default='')
@click.option('--reset', help='Resets the values in the configuration', default=False, is_flag=True)
@click.option('--echo', help='Echoes the updated configuration back to the console', default=False, is_flag=True)
def init(key, secret, sub, app, env, url, reset, echo):
    """Initializes the configuration.  Omitted parameters will leave those settings unchanged."""
    if not reset and config_exists():
        click.echo(click.style('Loading config.....', fg='yellow'))
        config = load_config()
    else:
        click.echo(click.style('Creating config.....', fg='yellow'))
        config = create_config()

    if key:
        config['credentials']['cloco_client_key'] = key
    if secret:
        config['credentials']['cloco_client_secret'] = secret
    if url:
        config['settings']['url'] = url
    if sub:
        config['preferences']['subscription'] = sub
    if app:
        config['preferences']['application'] = app
    if env:
        config['preferences']['environment'] = env
    save_config(config, False)
    if echo:
        print_config(config)
    return


@main.command()
def me():
    """Returns the current user's information."""
    config = load_config()
    authenticate(config)
    u = '{0}/me'.format(get_url(config))
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@main.group()
def subscription():
    """A subgroup of commands for subscriptions"""
    return


@subscription.command('list')
def list_subscriptions():
    """Returns a list of the subscriptions the current user has access to"""
    config = load_config()
    authenticate(config)
    r = requests.get(get_url(config), headers=get_headers(config))
    print_json_response(r)
    return


@subscription.command('create')
@click.option('--sub', help='The subscription identifier')
def create_subscription(sub):
    """Creates a subscription."""
    config = load_config()
    authenticate(config)
    body = {'subscriptionId': sub}
    u = '{0}/subscription'.format(get_url(config))
    r = requests.post(u, data=json.dumps(body), headers=get_headers(config))
    print_json_response(r)
    return


@subscription.command('get')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
def get_subscription(sub):
    """Retrieves the subscription"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    u = '{0}/{1}'.format(get_url(config), sub)
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@subscription.command('delete')
@click.option('--sub', help='The subscription identifier')
def delete_subscription(sub):
    """Deletes the subscription"""
    config = load_config()
    authenticate(config)
    u = '{0}/{1}'.format(get_url(config), sub)
    r = requests.delete(u, headers=get_headers(config))
    print_response(r)
    return


@subscription.group('permissions')
def subscription_permissions():
    """A subgroup of commands for subscription permissions"""
    return


@subscription_permissions.command('list')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
def list_subscription_permissions(sub):
    """Returns a list of the subscription permissions"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    u = '{0}/{1}/permissions'.format(get_url(config), sub)
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@subscription_permissions.command('create')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--username', help='The username to be added to the subscription')
@click.option('--admin', 'role', flag_value='admin', help='The user role (admin | user)')
@click.option('--user', 'role', flag_value='user', help='The user role (admin | user)', default=True)
def create_subscription_permission(sub, username, role):
    """Creates or modifies permissions in a subscription."""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    u = '{0}/{1}/permissions'.format(get_url(config), sub)
    body = {'permissionLevel': role, 'identity': username}
    r = requests.post(u, data=json.dumps(body), headers=get_headers(config))
    print_response(r)
    return


@subscription_permissions.command('delete')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--username', help='The username to be added to the subscription')
def delete_subscription_permission(sub, username):
    """Deletes the user from the subscription"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    u = '{0}/{1}/permissions/{2}'.format(get_url(config), sub, username)
    r = requests.delete(u, headers=get_headers(config))
    print_response(r)
    return


@main.group()
def application():
    """A subgroup of commands for applications"""


@application.command('list')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
def list_applications(sub):
    """Returns a list of the applications in the subscription"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    u = '{0}/{1}/applications'.format(get_url(config), sub)
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@application.command('get')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
def get_application(sub, app):
    """Retrieves the application metadata"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    u = '{0}/{1}/applications/{2}'.format(get_url(config), sub, app)
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@application.command('put')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--filename', help='The file containing the application JSON data')
def put_application(sub, app, filename):
    """Saves the application metadata"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not os.path.isfile(filename):
        click.echo(click.style(
            'File "{0}" not found'.format(filename), fg='red'))
        sys.exit('Invalid input.')
    with open(filename, 'r') as jsonfile:
        body = jsonfile.read()
        jsonfile.close()
    u = '{0}/{1}/applications/{2}'.format(get_url(config), sub, app)
    r = requests.put(u, headers=get_headers(config), data=body)
    print_response(r)
    return


@application.command('delete')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier')
def delete_application(sub, app):
    """Deletes the application"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    u = '{0}/{1}/applications/{2}'.format(get_url(config), sub, app)
    r = requests.delete(u, headers=get_headers(config))
    print_response(r)
    return


@application.group('permissions')
def application_permissions():
    """A subgroup of commands for application permissions"""
    return


@application_permissions.command('list')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
def list_application_permissions(sub, app):
    """Returns a list of the application permissions"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    u = '{0}/{1}/applications/{2}/permissions'.format(
        get_url(config), sub, app)
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@application_permissions.command('create')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--username', help='The username to be added to the subscription')
def create_application_permission(sub, app, username):
    """Creates or modifies permissions in an application."""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    u = '{0}/{1}/applications/{2}/permissions'.format(
        get_url(config), sub, app)
    body = {'permissionLevel': 'admin', 'identity': username}
    r = requests.post(u, data=json.dumps(body), headers=get_headers(config))
    print_response(r)
    return


@application_permissions.command('delete')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--username', help='The username to be added to the subscription')
def delete_application_permission(sub, app, username):
    """Deletes the user from the application"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    u = '{0}/{1}/applications/{2}/permissions/{3}'.format(
        get_url(config), sub, app, username)
    r = requests.delete(u, headers=get_headers(config))
    print_response(r)
    return


@main.group()
def configuration():
    """A subgroup of commands for configuration"""


@configuration.command('list')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
def list_configuration(sub, app):
    """Lists the configuration objects for an application"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    u = '{0}/{1}/configuration/{2}'.format(get_url(config), sub, app)
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@configuration.command('get')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--cob', help='The configuration object identifier')
@click.option('--env', help='The environment identifier, if not supplied will use the environment stored in preferences', default='')
@click.option('--raw', 'output', flag_value='raw', help='Return the raw configuration data with no decoding', default=True)
@click.option('--json', 'output', flag_value='json', help='Return the configuration metadata and data JSON')
def get_configuration(sub, app, cob, env, output):
    """Retrieves the configuration objects for an application"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not env:
        env = config['preferences']['environment']
    u = '{0}/{1}/configuration/{2}/{3}/{4}'.format(
        get_url(config), sub, app, cob, env)
    r = requests.get(u, headers=get_headers(config))
    if output == 'raw':
        if r.status_code == 200:
            payload = json.loads(r.text)
            encoded = payload['configurationData']
            click.echo(click.style(encoded, fg='green'))
        else:
            click.echo(click.style(r.text, fg='red'))
            sys.exit('Request failed.')
    else:
        print_json_response(r)
    return


@configuration.command('put')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--cob', help='The configuration object identifier')
@click.option('--env', help='The environment identifier')
@click.option('--filename', help='The file containing the configuration data', default='')
@click.option('--data', help='A raw string of configuration data', default='')
@click.option('--mime-type', help='The MIME type for the data, default to application/x-www-form-urlencoded', default='application/x-www-form-urlencoded')
def put_configuration(sub, app, cob, env, filename, data, mime_type):
    """Retrieves the application"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not env:
        env = config['preferences']['environment']
    if filename:
        if not os.path.isfile(filename):
            click.echo(click.style(
                'File "{0}" not found'.format(filename), fg='red'))
            sys.exit('Invalid input.')
        with open(filename, 'r') as jsonfile:
            body = jsonfile.read()
            jsonfile.close()
    else:
        if not data:
            click.echo(click.style('No filename or data found', fg='red'))
            sys.exit('Invalid input.')
        body = data
    u = '{0}/{1}/configuration/{2}/{3}/{4}'.format(
        get_url(config), sub, app, cob, env)
    r = requests.put(u, headers=get_headers_with_mime(
        config, mime_type), data=body)
    print_response(r)
    return


@configuration.group('version')
def configuration_versions():
    """A subgroup of commands for configuration version history"""


@configuration_versions.command('list')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--cob', help='The configuration object identifier')
@click.option('--env', help='The environment identifier, if not supplied will use the environment stored in preferences', default='')
def get_configuration_version_history(sub, app, cob, env):
    """Retrieves the configuration objects for an application"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not env:
        env = config['preferences']['environment']
    u = '{0}/{1}/configuration/versions/{2}/{3}/{4}'.format(
        get_url(config), sub, app, cob, env)
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@configuration_versions.command('get')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--cob', help='The configuration object identifier')
@click.option('--env', help='The environment identifier, if not supplied will use the environment stored in preferences', default='')
@click.option('--version', help='The version or revision number')
@click.option('--raw', 'output', flag_value='raw', help='Return the raw configuration data with no decoding', default=True)
@click.option('--json', 'output', flag_value='json', help='Return the configuration metadata and data JSON')
def get_configuration_version(sub, app, cob, env, version, output):
    """Retrieves the configuration objects for an application"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not env:
        env = config['preferences']['environment']
    u = '{0}/{1}/configuration/versions/{2}/{3}/{4}/{5}'.format(
        get_url(config), sub, app, cob, env, version)
    r = requests.get(u, headers=get_headers(config))
    if output == 'raw':
        if r.status_code == 200:
            payload = json.loads(r.text)
            encoded = payload['configurationData']
            click.echo(click.style(encoded, fg='green'))
        else:
            click.echo(click.style(r.text, fg='red'))
            sys.exit('Request failed.')
    else:
        print_json_response(r)
    return


@configuration_versions.command('restore')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--cob', help='The configuration object identifier')
@click.option('--env', help='The environment identifier, if not supplied will use the environment stored in preferences', default='')
@click.option('--version', help='The version or revision number')
def get_configuration_version(sub, app, cob, env, version):
    """Retrieves the configuration objects for an application"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not env:
        env = config['preferences']['environment']
    u = '{0}/{1}/configuration/versions/{2}/{3}/{4}/{5}'.format(
        get_url(config), sub, app, cob, env, version)
    r = requests.put(u, headers=get_headers(config))
    print_json_response(r)
    return


@configuration.group('permissions')
def configuration_permissions():
    """A subgroup of commands for configuration permissions"""


@configuration_permissions.command('list')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--cob', help='The configuration object identifier')
@click.option('--env', help='The environment identifier, if not supplied will use the environment stored in preferences', default='')
def list_configuration_permissions(sub, app, cob, env):
    """Returns a list of the application permissions"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not env:
        env = config['preferences']['environment']
    u = '{0}/{1}/configuration/{2}/{3}/{4}/permissions'.format(
        get_url(config), sub, app, cob, env)
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@configuration_permissions.command('create')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--cob', help='The configuration object identifier')
@click.option('--env', help='The environment identifier, if not supplied will use the environment stored in preferences', default='')
@click.option('--username', help='The username to be added to the subscription')
@click.option('--read', 'role', flag_value='read', help='The user role (read | write)', default=True)
@click.option('--write', 'role', flag_value='write', help='The user role (read | write)')
def create_configuration_permission(sub, app, cob, env, username, role):
    """Creates or modifies permissions on a configuration object."""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not env:
        env = config['preferences']['environment']
    u = '{0}/{1}/configuration/{2}/{3}/{4}/permissions'.format(
        get_url(config), sub, app, cob, env)
    body = {'permissionLevel': role, 'identity': username}
    r = requests.post(u, data=json.dumps(body), headers=get_headers(config))
    print_response(r)
    return


@configuration_permissions.command('delete')
@click.option('--sub', help='The subscription identifier, will use the subscription stored in the preferences if not supplied', default='')
@click.option('--app', help='The application identifier, will use the application stored in preferences if not supplied', default='')
@click.option('--cob', help='The configuration object identifier')
@click.option('--env', help='The environment identifier, if not supplied will use the environment stored in preferences', default='')
@click.option('--username', help='The username to be added to the subscription')
def delete_application_permission(sub, app, cob, env, username):
    """Deletes the user from the configuration"""
    config = load_config()
    authenticate(config)
    if not sub:
        sub = config['preferences']['subscription']
    if not app:
        app = config['preferences']['application']
    if not env:
        env = config['preferences']['environment']
    u = '{0}/{1}/configuration/{2}/{3}/{4}/permissions/{5}'.format(
        get_url(config), sub, app, cob, env, username)
    r = requests.delete(u, headers=get_headers(config))
    print_response(r)
    return


@main.group()
def credentials():
    """A subgroup of commands for subscriptions"""
    return


@credentials.command('list')
def list_credentials():
    """Returns a list of the credentials the current user has access to"""
    config = load_config()
    authenticate(config)
    u = '{0}/user/credentials'.format(get_url(config))
    r = requests.get(u, headers=get_headers(config))
    print_json_response(r)
    return


@credentials.command('create')
def create_credentials():
    """Creates client credentials."""
    config = load_config()
    authenticate(config)
    u = '{0}/user/credentials'.format(get_url(config))
    body = {'grant_type': 'client_credentials'}
    r = requests.post(u, data=json.dumps(body), headers=get_headers(config))
    print_json_response(r)
    return


@credentials.command('delete')
@click.option('--key', help='The client key of the credentials to be deleted')
def create_credentials(key):
    """Deletes client credentials."""
    config = load_config()
    authenticate(config)
    u = '{0}/user/credentials/{1}'.format(get_url(config), key)
    r = requests.delete(u, headers=get_headers(config))
    print_response(r)
    return

# common functions used by the api calls


def print_response(r):
    """Prints the HTTP response with formatting"""
    if r.status_code == 200:
        click.echo(click.style(r.text, fg='green'))
    else:
        click.echo(click.style(r.text, fg='red'))
        sys.exit('Request failed.')
    return


def print_json_response(r):
    """Prints the HTTP response with JSON formatting"""
    if r.status_code == 200:
        document = json.loads(r.text)
        click.echo(click.style(json.dumps(document, sort_keys=True,
                                          indent=4, separators=(',', ': ')), fg='green'))
    else:
        click.echo(click.style(r.text, fg='red'))
        sys.exit('Request failed.')
    return


def get_url(config):
    """Retrieves the url from configuration, else uses the default cloco url"""
    url = config['settings']['url']
    if not url:
        url = 'https://api.cloco.io'
    return url


def get_headers(config):
    """Gets the common HTTP headers"""
    return get_headers_with_mime(config, 'application/json')


def get_headers_with_mime(config, mime_type):
    """Gets the common HTTP headers"""
    token = config['credentials']['cloco_access_token']
    headers = {'content-type': mime_type, 'authorization': 'Bearer ' + token}
    return headers


def authenticate(config):
    """Authenticates using the stored credentials."""
    token = config['credentials']['cloco_access_token']
    if not is_token_valid(token):
        clientKey = config['credentials']['cloco_client_key']
        clientSecret = config['credentials']['cloco_client_secret']
        url = get_url(config)
        body = {'grant_type': 'client_credentials'}
        headers = {'content-type': 'application/json'}
        r = requests.post(url + '/oauth/token', data=json.dumps(body),
                          auth=HTTPBasicAuth(clientKey, clientSecret), headers=headers)
        if r.status_code == 200:
            payload = json.loads(r.text)
            token = payload['access_token']
            config['credentials']['cloco_access_token'] = token
            save_config(config, True)
        else:
            click.echo(click.style(r.text, fg='red'))
            sys.exit('Authentication failed.')
    return

# JWT functions


def is_token_valid(token):
    """Checks the access token to see if it has expired"""
    return False

# Configuration functions


def create_config():
    """Creates an empty configuration file for the instances when none exists"""
    config = configparser.ConfigParser()
    config['credentials'] = {}
    config['credentials']['cloco_client_key'] = ''
    config['credentials']['cloco_client_secret'] = ''
    config['credentials']['cloco_access_token'] = ''
    config['settings'] = {}
    config['settings']['url'] = ''
    config['preferences'] = {}
    config['preferences']['subscription'] = ''
    config['preferences']['application'] = ''
    config['preferences']['environment'] = ''
    return config


def print_config(config):
    click.echo(click.style('Current configuration:', fg='white'))
    click.echo(click.style(' ', fg='white'))
    for section in config:
        click.echo(click.style('[{0}]'.format(section), fg='white'))
        for key in config[section]:
            click.echo(click.style(key + ' = ' +
                                   config[section][key], fg='cyan'))
        click.echo(click.style(' ', fg='white'))


def load_config():
    """Loads the configuration from the ini file."""
    if not config_exists():
        click.echo(click.style(
            'Configuration not available.  Run cloco init to initialize config.', fg='red'))
        sys.exit('Configuration error.')
    config = configparser.ConfigParser()
    config.read(get_config_path())
    return config


def save_config(config, silent):
    """Saves the configuration object to disk"""
    if not silent:
        click.echo(click.style('Saving config.....', fg='yellow'))
    with open(get_config_path(), 'w') as configfile:
        config.write(configfile)
        configfile.close()
    return


def config_exists():
    """Returns a Boolean value indicating whether the config file exists"""
    return os.path.isfile(get_config_path())


def get_config_path():
    """Retrieves the config folder for the current user."""
    return '{0}/.cloco/configuration'.format(os.environ["HOME"])
