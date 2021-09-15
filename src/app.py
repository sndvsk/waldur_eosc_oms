import logging
import utils_orders as utils_orders
import utils_offers as utils_offers


logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                               f'%(message)s')


def sync_orders():
    utils_orders.process_orders()
    logging.info('process_orders is finished.')
    return "The orders were synced"


def sync_offers():
    utils_offers.process_offers()
    logging.info('process_offers is finished.')
    return "Offerings have been processed"


if __name__ == '__main__':
    sync_orders()
