import logging
import utils_orders as u_orders
# import utils_offers as u_offers


logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                               f'%(message)s')


def sync_orders():
    u_orders.process_orders()
    logging.info('process_orders is finished.')
    return "The orders were synced"


if __name__ == '__main__':
    sync_orders()
