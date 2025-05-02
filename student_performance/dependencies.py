from sessions import ChanzoAgentDbSession, ChanzoAppDbSession


def get_chanzo_agent_db_session():
    db = ChanzoAgentDbSession()
    try:
        yield db
    finally:
        db.close()


def get_chanzo_app_db_session():
    db = ChanzoAppDbSession()
    try:
        yield db
    finally:
        db.close()
