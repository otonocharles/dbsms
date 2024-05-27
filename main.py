from get_data import DatabaseManager
from config import Db_Config, Message
import time
from apscheduler.schedulers.background import BackgroundScheduler
import logging



def main():
     logging.basicConfig(level=logging.INFO)
     logger = logging.getLogger(__name__)

    # Create a file handler and set its formatter
     file_handler = logging.FileHandler('scheduler.log')
     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
     file_handler.setFormatter(formatter)

    # Add the file handler to the logger
     logger.addHandler(file_handler)
    # Initialize configuration, message, and database manager
     config = Db_Config()
     message = Message()
     db_manager = DatabaseManager(config, message)

    # Initialize scheduler
     schedule = BackgroundScheduler(daemon=True, timezone='Africa/Lagos')

    # Add job to scheduler
     schedule.add_job(
        db_manager.perform_opeartion,
        'cron',
        day='*',
        hour='5,7,13,19',
        minute='15',
        misfire_grace_time=300,
        coalesce=True
    )

    # Start scheduler
     schedule.start()
     logger.info("Scheduler started.")

    # Print scheduled jobs
     schedule.print_jobs()

     try:
        # Keep the script running
        while True:
            time.sleep(1)
     except (KeyboardInterrupt, SystemExit):
        # Shut down the scheduler on exit
        schedule.shutdown()
        logger.info("Scheduler stopped.")

if __name__ == "__main__":
    main()