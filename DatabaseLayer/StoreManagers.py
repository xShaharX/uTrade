from DatabaseLayer.getConn import commit_command, select_command
from SharedClasses.StoreManager import StoreManager


def parse_store_managers(store_managers):
    store_managers_list = []
    for store_manager in store_managers:
        store_managers_list.append(StoreManager(store_manager[0], store_manager[1], store_manager[2],
                                                store_manager[3], store_manager[4], store_manager[5],
                                                store_manager[6], store_manager[7], store_manager[8], store_manager[9]))
    return store_managers_list


def get_store_manager(username, shop_name):
    sql_query = """
                SELECT *
                FROM StoreManagers
                WHERE username = '{}' AND shop_name = '{}'
            """.format(username, shop_name)
    manager = select_command(sql_query)
    manager = parse_store_managers(manager)
    if len(manager) == 1:
        return manager[0]
    else:
        return False


def is_store_manager(username):
    sql_query = """
                SELECT *
                FROM StoreManagers
                WHERE username = '{}'
            """.format(username)
    manager = select_command(sql_query)
    manager = parse_store_managers(manager)
    if len(manager) >= 1:
        return True
    else:
        return False


def add_manager(store_manager):
    sql = """
            INSERT INTO StoreManagers (username, shop_name, 
                                        addItemPermission,
                                        removeItemPermission,
                                        editItemPermission,
                                        replyMessagePermission, 
                                        getAllMessagePermission,
                                        getPurchaseHistoryPermission,
                                        discountPermission,
                                        setPolicyPermission)
            VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
            """.format(store_manager.username, store_manager.store_name,
                       store_manager.permission_add_item,
                       store_manager.permission_remove_item,
                       store_manager.permission_edit_item,
                       store_manager.permission_reply_messages,
                       store_manager.permission_get_all_messages,
                       store_manager.permission_get_purchased_history,
                       store_manager.discount_permission,
                       store_manager.permission_set_policy)
    return commit_command(sql)


def remove_manager(username):
    sql = """
                    DELETE FROM StoreManagers
                    WHERE username = '{}'
                  """.format(username)
    return commit_command(sql)


def remove_manager_from_shop(username, shop_name):
    sql = """
                        DELETE FROM StoreManagers
                        WHERE username = '{}' AND shop_name = '{}'
                      """.format(username, shop_name)
    return commit_command(sql)


def get_manager_shops(username):
    sql_query = """
                    SELECT *
                    FROM StoreManagers
                    WHERE username = '{}'
                """.format(username)
    manager = select_command(sql_query)
    return parse_store_managers(manager)


def get_store_managers_on_shop(shop_name):
    sql_query = """
                        SELECT *
                        FROM StoreManagers
                        WHERE shop_name = '{}'
                    """.format(shop_name)
    managers = select_command(sql_query)
    return parse_store_managers(managers)


def update_permissions(store_manager):
    sql_query = """
                UPDATE StoreManagers 
                SET addItemPermission = '{}'  ,removeItemPermission ='{}'   ,editItemPermission  ='{}', 
                replyMessagePermission ='{}' ,getAllMessagePermission ='{}', getPurchaseHistoryPermission='{}' 
                ,discountPermission ='{}', setPolicyPermission='{}'
                WHERE username='{}' AND shop_name = '{}'
                """.format(store_manager.permission_add_item,
                           store_manager.permission_remove_item,
                           store_manager.permission_edit_item,
                           store_manager.permission_reply_messages,
                           store_manager.permission_get_all_messages,
                           store_manager.permission_get_purchased_history,
                           store_manager.discount_permission,
                           store_manager.permission_set_policy,
                           store_manager.username,
                           store_manager.store_name)
    return commit_command(sql_query)


def is_store_manager_of_shop(username, shop_name):
    return get_store_manager(username, shop_name) is not False
