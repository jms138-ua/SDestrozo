"""
client.send_msg("Create"|"Delete")
client.send_obj(("user","password"))
client.recv_msg() -> MSGOPRE

//////////////////////////////////////////

client.send_msg("Update")
client.send_obj(("user","password"))
client.send_obj(("newuser","newpassword"))
client.recv_msg() -> MSGOPRE
"""

from common_utils import MySocket, rundb

from dataclasses import dataclass
import sys


ADDR = ("", int(sys.argv[1]))

FDATA_DB = "../data/db.db"

MSGOP_CREATED = "Usuario creado"
MSGOP_UPDATED = "Usuario actualizado"
MSGOP_DELETED = "Usuario eliminado"
MSGOP_ALREADY_EXISTS = "El ususario ya existe"
MSGOPRE_NOT_EXIST = "La cuenta no coincide con ninguna registrada"
MSGOPRE_ERROR = "Operacion no permitida"


@dataclass
class User:
    alias: str
    password: str


def create_db():
    rundb(FDATA_DB,
        """
        CREATE TABLE IF NOT EXISTS players(
            alias VARCHAR[50] PRIMARY KEY,
            password VARCHAR[50] NOT NULL
        )
        """
    )

def select_user_db(alias):
    res = rundb(FDATA_DB,
        """
        SELECT alias, password
        FROM players
        WHERE alias = ?
        """
        ,(alias,)
    )
    user = res.fetchone()
    return None if user is None else User(*user)

def create_user_db(user):
    if select_user_db(user.alias) is not None:
        return False

    rundb(FDATA_DB,
        """
        INSERT INTO players
        VALUES(?, ?)
        """
        ,(user.alias, user.password)
    )
    return True

def update_user_db(alias, user):
    if select_user_db(alias) is None:
        return False

    rundb(FDATA_DB,
        """
        UPDATE players
        SET alias = ?, password = ?
        WHERE alias = ?
        """
        ,(user.alias, user.password, alias)
    )
    return True

def delete_user_db(alias):
    if select_user_db(alias) is None:
        return False

    rundb(FDATA_DB,
        """
        DELETE
        FROM players
        WHERE alias = ?
        """
        ,(alias,)
    )
    return True

def user_correct_login_db(user):
    user_fetch = select_user_db(user.alias)
    return user_fetch is not None and user_fetch.password == user.password

#==================================================

with MySocket("TCP", ADDR) as server:
    create_db()

    while True:
        conn, direcc = server.accept()
        op = server.recv_msg()
        user = User(*server.recv_obj())
        print(direcc, "Solicita", op, "sobre", user)

        if op == "Create":
            iscreated = create_user_db(user)
            server.send_msg(
                MSGOP_CREATED if iscreated
                else MSGOP_ALREADY_EXISTS
            )
            if isdeleted:
                print(direcc, "Ha creado el usaurio")

        elif op == "Update":
            if user_correct_login_db(user):
                newuser = User(*server.recv_obj())
                if newuser != user:
                    isupdated = update_user_db(user.alias, newuser)
                    server.send_msg(
                        MSGOP_UPDATED if isupdated
                        else MSGOP_ALREADY_EXISTS
                    )
                    if isupdated:
                        print(direcc, "Ha cambiado el usuario a", newuser)
                else:
                    server.send_msg(MSGOP_ALREADY_EXISTS)
            else:
                server.send_msg(MSGOPRE_NOT_EXIST)

        elif op == "Delete":
            if user_correct_login_db(user):
                isdeleted = delete_user_db(user.alias)
                server.send_msg(
                    MSGOP_DELETED if isdeleted
                    else MSGOP_NOT_EXIST
                )
                if isdeleted:
                    print(direcc, "Ha eliminado el usaurio")
            else:
                server.send_msg(MSGOPRE_NOT_EXIST)

        else:
            server.send_msg(MSGOP_ERROR)

        conn.close()