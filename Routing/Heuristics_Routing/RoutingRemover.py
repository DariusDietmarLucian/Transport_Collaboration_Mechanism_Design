class RoutingRemover:
    """
    ***********
    ***PUBLIC***
    ***********
    """

    @staticmethod
    def remove_single_request(route, request):
        p_node = request.get_pickup_node()
        d_node = request.get_delivery_node()
        new_route = [node for node in route if node.id is not p_node.id and node.id is not d_node.id].copy()

        return new_route

    @staticmethod
    def remove_multiple_requests(route, requests):
        new_route = route.copy()

        for request in requests:
            new_route = RoutingRemover.remove_single_request(route=new_route, request=request)

        return new_route
