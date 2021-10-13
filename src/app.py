import logging
import utils_orders


logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=f'[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - '
                                               f'%(message)s')


def sync_orders():
    utils_orders.process_orders()
    logging.info('process_orders is finished.')
    return "The orders were synced"


if __name__ == '__main__':
    sync_orders()
