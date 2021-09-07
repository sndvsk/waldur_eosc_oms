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


def sync_offerings():
    utils_offers.process_offerings()
    logging.info('process_resources is finished.')
    return "Offerings have been processed"


if __name__ == '__main__':
    sync_orders()


# # Time
# schedule.every(20).seconds.do(sync_projects)
# schedule.every(30).seconds.do(process_orders)
#
#
# try:
#     while True:
#         schedule.run_pending()
#         time.sleep(30)
# except KeyboardInterrupt:
#     print('Interrupted!')
