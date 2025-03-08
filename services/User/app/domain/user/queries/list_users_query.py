from app.domain.mixins.pagination import PaginationParams


class ListUsersQuery:
    def __init__(self, pagination: PaginationParams):
        self.pagination = pagination
