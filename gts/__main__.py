# import runpy

from gts import gts_logger
from gts.test import test_obj_import
# import gts.test.test_obj_import as tob


if __name__ == '__main__':
    gts_logger.info(" ∫ starting obj load test")
    test_obj_import.main()
    gts_logger.info(" ∫ finished test")
