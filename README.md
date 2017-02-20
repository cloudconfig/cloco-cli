<p align="center">
  <img src="https://raw.githubusercontent.com/cloudconfig/cloco-docs/master/source/images/logo.png" width="100" height="104" />
</p>

# cloco cli

A command line interface for the cloco API.

# Installation

To install with pip:

    $ pip install cloco-cli

## Prerequisites

This script is designed for a linux shell.  It may work on a Windows shell but is not supported.

The cloco CLI is written in Python 2.6+.

Before you can use this script you will need to have registered on cloco [https://www.cloco.io](https://www.cloco.io) and generated API credentials.  You will need these credentials when initializing the CLI.

# Documentation

Please read the documentation for the cloco API and the cloco CLI at [https://docs.cloco.io/](https://docs.cloco.io/).

# Help

To access the top-level help menu:

$ cloco --help

# Initialization

Before you use the cloco-cli to access the API you must initialize the configuration.  The minimum you must provide are the API credentials.

$ cloco init --key <client key> --secret <client secret> [--url <api url>] [--sub <subscription identifier>] [--app <application identifier>] [--env <environment identifier>] [--reset]

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--key | The client key of the API credentials. | Must be supplied for the CLI to access the API.
--secret | The client secret of the API credentials. | Must be supplied for the CLI to access the API.
--sub | The ID of the subscription. | Optional, but if not set you will need to supply --sub in subsequent API calls.
--app | The ID of the application. | Optional, but if not set you will need to supply --app in subsequent API calls.
--env | The ID of the environment. | Optional, but if not set you will need to supply --env in subsequent API calls.
--url | The URL of the cloco API. | Optional, intended for on-premise installs.  Will default to the hosted cloco API [https://api.cloco.io](https://api.cloco.io).
--reset | Flag. | Resets all values back to the default (i.e. blank) and sets only those supplied.

# Personal Information

To retrieve your cloco profile:

$ cloco me

### Parameters

None.

# Subscription

When you sign up for a subscription in cloco it allows you to manage all your application metadata in one place.

## List Your Subscriptions

To list the subscriptions you have access to:

$ cloco subscription list

### Parameters

None.

## Retrieve a Subscription

To retrieve the metadata for a subscription (must be an admin):

$ cloco subscription get --sub <subscription identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.

## Create a Subscription

To create a new subscription:

$ cloco subscription create --sub <subscription identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Required.  As this is a critical operation the cli will not use the configured value.

## Delete a Subscription

To delete a subscription and all associated data (must be an admin):

$ cloco subscription delete --sub <subscription identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Required.  As this is a critical operation the cli will not use the configured value.

## List Subscription Permissions

Depending on your subscription level, you can have multiple users associated with a subscription.  To view the permissions associated with the subscription:

$ cloco subscription permissions list --sub <subscription identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.

## Create / Modify Subscription Permissions

To add or modify the permissions of a user on the subscription:

$ cloco subscription permissions create --sub <subscription identifier> --username <username> [--admin | --user]

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--username | The username to permission. | Required. The username in cloco.
--admin / --user | Flag. | The permission level to assign.  Defaults to 'user'.

## Revoke Subscription Permissions

To revove all permissions for a user on the subscription:

$ cloco subscription permissions delete --sub <subscription identifier> --username <username>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--username | The username to permission. | Required. The username in cloco.

# Application

An application in cloco maps onto an application you are developing or a DevOps project you are building.  This allows you to group together related configuration.

The application metadata is important for cloco in allowing us to store and retrieve configuration.  The application defines which configuration objects you wish to store and which environments you wish to hold configuration for.

## List Applications

To retrieve the applications within a subscription:

$ cloco application list --sub <subscription identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.

## Retrieve an Application

To retrieve the application metadata:

$ cloco application get --sub <subscription identifier> --app <application identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.

## Create / Update an Application

To store the application metadata:

$ cloco application put --sub <subscription identifier> --app <application identifier> --filename <path to file>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--filename | The path to a data file. | Required.  The file should contain valid metadata for the application.

## Delete an Application

To delete the application metadata and associated configuration:

$ cloco application delete --sub <subscription identifier> --app <application identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Required.  As this is a critical operation the application identifier must be supplied.

## List Application Permissions

All subscription admins can administer applications.  If you would like to permission a user to administer a single application they must first be added to the subscription with user permissions and then permissioned on the application.  The only available permission at application level is administrator.

To list permissions on an application:

$ cloco application permissions list --sub <subscription identifier> --app <application identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.

## Create / Modify Application Permissions

To create or update permissions on an application:

$ cloco application permissions create --sub <subscription identifier> --app <application identifier> --username <username>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--username | The username to permission. | Required. The username in cloco.

## Revoke Application Permissions

If you revoke permissions for a user on an application they will still be registered as a user in the subscription.  

To create or update permissions on an application:

$ cloco application permissions delete --sub <subscription identifier> --app <application identifier> --username <username>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--username | The username to permission. | Required. The username in cloco.

# Configuration

Configuration is what cloco is all about.  Subscriptions and applications make it easier to manage and permission you configuration data.  This section allows you to manage configuration more directly.

## List Configuration

To view the configuration stored in an application:

$ cloco configuration list --sub <subscription identifier> --app <application identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.

## Retrieve Configuration

To retrieve configuration saved for a specific environment:

$ cloco configuration get --sub <subscription identifier> --app <application identifier>  --cob <configuration object identifier> --env <environment identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--cob | The ID of the configuration object. | Required.  This must be one of the configuration object specified in the application.
--env | The ID of the application. | Optional if defaulted via the cloco init command.
--raw / --json | Flag. | Indicates how you want the response.  --raw will return the data as uploaded, --json will return your configuration as a JSON packet along with the associated metadata.

## Create / Update Configuration

To store configuration data:

$ cloco configuration put --sub <subscription identifier> --app <application identifier> --cob <configuration object identifier> --env <environment identifier> [--filename <path to file>] [--data <raw data>]

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--cob | The ID of the configuration object. | Required.  This must be one of the configuration object specified in the application.
--env | The ID of the application. | Optional if defaulted via the cloco init command.
--filename | The path to a data file. | Required if data not supplied.  The file contains the data that will be stored in cloco.
--data | A string of raw data to upload. | Required if filename not supplied.
--mime-type | The MIME type of the data to upload. | Optional.  Defaults to 'application/x-www-form-urlencoded' to send text.

## List Configuration Versions

To list the version history for configuration, for a specific environment:

$ cloco configuration versions list --sub <subscription identifier> --app <application identifier> --cob <configuration object identifier> --env <environment identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--cob | The ID of the configuration object. | Required.  This must be one of the configuration object specified in the application.
--env | The ID of the application. | Optional if defaulted via the cloco init command.

## Retrieve a Configuration Version

To retrieve a specific version from the history:

$ cloco configuration versions get --sub <subscription identifier> --app <application identifier> --cob <configuration object identifier> --env <environment identifier> --version <version>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--cob | The ID of the configuration object. | Required.  This must be one of the configuration object specified in the application.
--env | The ID of the application. | Optional if defaulted via the cloco init command.
--version | The version number. | Required.

## Restore a Configuration Version

To reinstate a previous version of configuration as the current version:

$ cloco configuration versions restore --sub <subscription identifier> --app <application identifier> --cob <configuration object identifier> --env <environment identifier> --version <version>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--cob | The ID of the configuration object. | Required.  This must be one of the configuration object specified in the application.
--env | The ID of the application. | Optional if defaulted via the cloco init command.
--version | The version number. | Required.

## List Configuration Permissions

You can limit the permissions for any user to read or write configuration.  To permission a user on configuration they must first be added to the subscription as a user.  You can then grant them access to specific configuration in a specific environment.  Use this to permission service accounts for specific environments.

To list permissions on configuration:

$ cloco configuration permissions list --sub <subscription identifier> --app <application identifier> --cob <configuration object identifier> --env <environment identifier>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--cob | The ID of the configuration object. | Required.  This must be one of the configuration object specified in the application.
--env | The ID of the application. | Optional if defaulted via the cloco init command.

## Create / Modify Configuration Permissions

To create or update permissions on configuration:

$ cloco configuration permissions create --sub <subscription identifier> --app <application identifier> --cob <configuration object identifier> --env <environment identifier> --username <username> [--read | --write]

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--cob | The ID of the configuration object. | Required.  This must be one of the configuration object specified in the application.
--env | The ID of the application. | Optional if defaulted via the cloco init command.
--username | The username to permission. | Required. The username in cloco.
--read / --write | Flag. | Indicates the level of permission on the configuration.  Write permissions can also read.

## Revoke Configuration Permissions

If you revoke permissions for a user on configuration they will still be registered as a user in the subscription.  

To create or update permissions on configuration:

$ cloco configuration permissions delete --sub <subscription identifier> --app <application identifier> --cob <configuration object identifier> --env <environment identifier> --username <username>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--sub | The ID of the subscription. | Optional if defaulted via the cloco init command.
--app | The ID of the application. | Optional if defaulted via the cloco init command.
--cob | The ID of the configuration object. | Required.  This must be one of the configuration object specified in the application.
--env | The ID of the application. | Optional if defaulted via the cloco init command.
--username | The username to permission. | Required. The username in cloco.

# Credentials

The credentials routes in the API allow you to view and list API credentials that correspond to your identity.

## List API Credentials

To list the credentials already created under your username:

$ cloco credentials list

### Parameters

None.


## Create API Credentials

To create a new set of API credentials:

$ cloco credentials create

Note that the response from this API call is the only time you are ever given the client secret.  You must save the client key and client secret as a pair in order to use them later.

### Parameters

None.

## Revoke Credentials

To revoke credentials and prevent them from being used again:

$ cloco credentials revoke --key <client key>

### Parameters

Parameter | Description | Usage
--------- | ----------- | -----
--key | The client key of the credentials. | Required.
