from shared.mixins import PaginationParams


class ListUsersQuery:
    def __init__(self, pagination: PaginationParams):
        self.pagination = pagination
