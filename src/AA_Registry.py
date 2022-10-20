from common_utils import MySocket, rundb

from dataclasses import dataclass
import sys


ADDR = ("", int(sys.argv[1]))

FDATA_DB = "../data/db.db"


OPMSG_CREATED = "Usuario creado"
OPMSG_UPDATED = "Usuario actualizado"
OPMSG_DELETED = "Usuario eliminado"
OPMSG_ALREADY_EXISTS = "El ususario ya existe"
OPMSG_NOT_EXIST = "El ususario no existe"
OPMSG_ERROR = "Operacion no permitida"


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
    if select_user_db(alias) is not None:
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
    if select_user_db(alias) is not None:
        return False

    rundb(FDATA_DB,
        """
        DELETE
        FROM players
        WHERE alias = ?
        """
        ,(alias)
    )
    return True

#==================================================

with MySocket("TCP", ADDR) as server:
    create_db()

    while True:
        conn, direcc = server.accept()
        op = server.recv_msg()
        print(direcc, "Solicita ", op)

        user = User(*server.recv_msg())
        if op == "Create":
            iscreated = create_user_db(user)
            server.send_msg(
                OPMSG_CREATED if iscreated
                else OPMSG_ALREADY_EXISTS
            )

        elif op == "Update":
            newuser = User(*server.recv_msg())
            isupdated = update_user_db(user.alias, newuser)
            server.send_msg(
                OPMSG_UPDATED if isupdated
                else OPMSG_NOT_EXIST
            )

        elif op == "Delete":
            isdeleted = delete_user_db(user.alias)
            server.send_msg(
                OPMSG_DELETED if iscreated
                else OPMSG_NOT_EXIST
            )
        else:
            server.send_msg(OPMSG_ERROR)

        conn.close()