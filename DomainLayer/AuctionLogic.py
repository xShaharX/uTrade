from DatabaseLayer import Auctions


def bid_on_item(auction_bid):
    if auction_bid is not None:
        if auction_bid.price > Auctions.get_max_bid(auction_bid.auction_id):
            return Auctions.bid_on_item(auction_bid)
    return False


def add_auction(auction):
    if auction is not None:
        return Auctions.add_auction(auction)
    return False
