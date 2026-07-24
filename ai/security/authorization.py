class Authorization:


    def __init__(self):

        self.permissions = {


            "admin":

                [

                    "*"

                ],


            "agent":

                [

                    "execute_task",

                    "execute_tool",

                    "read_memory"

                ],


            "readonly":

                [

                    "read_memory"

                ]

        }



    def allowed(
        self,
        role,
        action
    ):


        permissions = self.permissions.get(
            role,
            []
        )


        return (

            "*"
            in
            permissions

            or

            action
            in
            permissions

        )



    def add_permission(
        self,
        role,
        permission
    ):


        if role not in self.permissions:

            self.permissions[
                role
            ] = []


        self.permissions[
            role
        ].append(
            permission
        )



    def get_role_permissions(
        self,
        role
    ):

        return self.permissions.get(
            role,
            []
        )
