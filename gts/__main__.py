import runpy

from gts import gts_logger
# import gts.test.test_obj_import as tob


if __name__ == '__main__':
    gts_logger.info(" ∫ starting obj load test")
    try:
        runpy.run_module('gts.test.test_obj_import')
    except SystemExit:
        gts_logger.info(" ∫ finished test")
        exit()
