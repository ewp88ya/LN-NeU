import time
import uuid


class Authentication:


    def __init__(self):

        self.sessions = {}



    def create_session(
        self,
        user_id,
        role="agent"
    ):

        session_id = str(
            uuid.uuid4()
        )


        session = {

            "session_id":
                session_id,

            "user_id":
                user_id,

            "role":
                role,

            "created_at":
                time.time()

        }


        self.sessions[session_id] = session


        return session



    def validate(
        self,
        session_id
    ):

        return self.sessions.get(
            session_id
        )



    def revoke(
        self,
        session_id
    ):

        if session_id in self.sessions:

            del self.sessions[
                session_id
            ]

            return True


        return False



    def active_sessions(
        self
    ):

        return list(
            self.sessions.values()
        )
