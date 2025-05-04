from engines import chanzo_agent_db_engine, chanzo_app_db_engine
from sqlalchemy.orm import sessionmaker

ChanzoAgentDbSession = sessionmaker(bind=chanzo_agent_db_engine)
ChanzoAppDbSession = sessionmaker(bind=chanzo_app_db_engine)
