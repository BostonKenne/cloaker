from dataclasses import dataclass
import asyncio
import http
import requests
import uvloop
import json


@dataclass
class KeycloakConnect(object):

    grant_type: str = "password"

    @classmethod
    async def __access_token(cls, url: str, client_id: str, client_secret: str,
                            username: str, password: str, scope: [],  grant_type: str = grant_type):
        try:
            url = url + "/realms/GoTest/protocol/openid-connect/token"
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            }
            # Expected body data
            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "username": username,
                "password": password,
                "scope": scope,
                "grant_type": grant_type,
            }
            handler = requests.post(url=url, data=data, headers=headers)
            return handler.content
        except Exception as e:
            return {"message": "Server Error " + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    # protect method access token get async method and provide await results.
    @classmethod
    async def _access_token(cls, url: str, client_id: str, client_secret: str,
                            username: str, password: str, grant_type: str, scope: []):
        try:
            result = asyncio.create_task(cls.__access_token(url=url, client_id=client_id, client_secret=client_secret,
                                                             username=username, password=password, grant_type=grant_type,
                                                             scope=scope))
            await asyncio.wait([result])
            return result
        except Exception as e:
            return {"message": "Server Error " + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    # Publicly accessible method
    @classmethod
    def access_token(cls, url: str, client_id: str, client_secret: str,
                     username: str, password: str, grant_type: str, scope: []):
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(cls._access_token(
                url=url, client_id=client_id, client_secret=client_secret,
                username=username, password=password, grant_type=grant_type, scope=scope
            )).result()
            return result
        except Exception as e:
            return {"message": "Server Error -> " + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value
        finally:
            loop.close()

    """ Handling account creation """
    @classmethod
    async def __create_account(cls, url: str, access_token: str, username: str, firstname: str,
                       lastname: str, email: str, realm_roles: [], groups: [], enabled: bool = True):
        try:
            if not access_token:
                return {"message": "Access Token is required"}, http.HTTPStatus.PRECONDITION_REQUIRED.value
            url = url + "/admin/realms/GoTest/users"
            headers = {
                "Authorization": "Bearer " + access_token,
            }
            data = {
                "username": username,
                "firstName": firstname,
                "lastName": lastname,
                "email": email,
                "realmRoles": realm_roles,
                "groups": groups,
                "enabled": enabled
            }
            handler = requests.post(url=url, json=data, headers=headers)
            await asyncio.sleep(0.005)
            return handler.content
        except Exception as e:
            return {"message": "Server Error -> " + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    @classmethod
    async def _create_account(cls, url: str, access_token: str, username: str, firstname: str,
                       lastname: str, email: str, realm_roles: [], groups: [], enabled: bool = True):
        try:
            result = asyncio.create_task(cls.__create_account(url=url, access_token=access_token, username=username,
                                                             firstname=firstname, lastname=lastname, email=email,
                                                             realm_roles=realm_roles, groups=groups, enabled=enabled))
            await asyncio.wait([result])
            return result
        except Exception as e:
            return {"message": "Server Error -> " + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    @classmethod
    def create_account(cls, url: str, access_token: str, username: str, firstname: str,
                       lastname: str, email: str, realm_roles: [], groups: [], enabled: bool = True):
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Mandatory uri
            if not url:
                return {"message": "Path uri is required"}, http.HTTPStatus.PRECONDITION_REQUIRED.value
            # Mandatory access token
            if not access_token:
                return {"message": "Access token is required"}, http.HTTPStatus.PRECONDITION_REQUIRED.value
            result = loop.run_until_complete(
                cls._create_account(url=url, access_token=access_token, username=username, firstname=firstname,
                                    lastname=lastname, email=email, realm_roles=realm_roles, groups=groups,
                                    enabled=enabled)
            ).result()
            return result
        except Exception as e:
            return {"message": "Server Error -> " + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value
        finally:
            loop.close()

    """ Fetch User """
    """
    :: Requirements
    - url -> base url = http://domain/auth not slash at end
    - access token -> mandatory
    - username -> not mandatory
    - firstname -> not mandatory
    - lastname -> not mandatory
    - email -> not mandatory
    """
    @classmethod
    async def __fetch_users(cls, url: str, access_token: str, username: str, firstname: str, lastname: str, email: str):
        try:
            url = url + "/admin/realms/GoTest/users"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            # Expected body data
            data = {
                "username": username,
                "firstName": firstname,
                "lastName": lastname,
                "email": email,
            }
            handler = requests.get(url=url, params=data, headers=headers)
            await asyncio.sleep(0.005)
            return handler.json()
        except Exception as e:
            return {"message": "Server Error -> A " + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    @classmethod
    async def _fetch_users(cls, url: str, access_token: str, username: str, firstname: str, lastname: str, email: str):
        try:
            result = asyncio.create_task(cls.__fetch_users(url=url, access_token=access_token,
                                                             username=username, firstname=firstname,
                                                             lastname=lastname, email=email))
            await asyncio.wait([result])
            return result
        except Exception as e:
            return {"message": "Server Error -> B" + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    @classmethod
    def fetch_users(cls, url: str, access_token: str = None, username: str = None,
                      firstname: str = None, lastname: str = None, email: str = None):
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(cls._fetch_users(url=url, access_token=access_token,
                                                                username=username, firstname=firstname,
                                                                lastname=lastname, email=email)).result()
            return result
        except Exception as e:
            return {"message": "Server Error -> C" + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value
        finally:
            loop.close()

    """ Deleting or removing users """
    """
    :: Requirements
    - url -> base url = http://domain/auth not slash at end
    - access token -> mandatory
    - user_id -> not mandatory
    """
    @classmethod
    async def __delete_users(cls, url: str, access_token: str, user_id: str):
        try:
            url = url + "/admin/realms/GoTest/users/" + f"{user_id}"
            headers = {
                "Authorization": "Bearer " + access_token
            }
            handler = requests.delete(url=url, headers=headers)
            await asyncio.sleep(0.005)
            if int(handler.status_code) == 204:
                return {"message": "Successfully deleted"}
        except Exception as e:
            return {"message": "Server Error -> A" + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    @classmethod
    async def _delete_users(cls, url: str, access_token: str, user_id: str):
        try:
            result = asyncio.create_task(cls.__delete_users(url=url, access_token=access_token, user_id=user_id))
            await asyncio.wait([result])
            return result
        except Exception as e:
            return {"message": "Server Error -> B" + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    @classmethod
    def delete_users(cls, url: str, access_token: str, user_id: str):
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                cls._delete_users(url=url, access_token=access_token, user_id=user_id)
            ).result()
            return result
        except Exception as e:
            return {"message": "Server Error -> C" + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value
        finally:
            loop.close()

    """ Update users """
    """
    :: Requirements
    - url -> base url = http://domain/auth not slash at end
    - access token -> mandatory
    - user_id -> not mandatory
    """
    """ Deleting or removing users """
    @classmethod
    async def __update_users(cls, url: str, access_token: str):
        try:
            await asyncio.sleep(0.005)
            pass
        except Exception as e:
            return {"message": "Server Error -> A" + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    @classmethod
    async def _update_users(cls, url: str, access_token: str):
        try:
            result = asyncio.create_task(cls.__update_users(url=url, access_token=access_token))
            await asyncio.wait([result])
            return result
        except Exception as e:
            return {"message": "Server Error -> B" + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value

    @classmethod
    def update_users(cls, url: str, access_token: str):
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete().result()
            return result
        except Exception as e:
            return {"message": "Server Error -> C" + str(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR.value
        finally:
            loop.close()