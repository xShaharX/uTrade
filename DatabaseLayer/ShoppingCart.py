from DatabaseLayer.getConn import getConn


def remove_item_from_cart(username, item_id):
    c = getConn().cursor()
    c.execute("""
                DELETE FROM ShoppingCart
                WHERE userName = {} AND itemId = {}
              """.format(username, item_id))
    return c.fetchall()


def browse_cart(username):
    c = getConn().cursor()
    c.execute("""
                SELECT *
                FROM ShoppingCart
                WHERE userName = {}
              """.format(username))
    return c.fetchall()