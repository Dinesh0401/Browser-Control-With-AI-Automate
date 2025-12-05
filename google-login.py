"""
CLI entry point for Google Sheet Expense Agent.
Run this to test browser automation from the command line.
"""

import logging
from run import run_agent_sync

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 60)
    logger.info("🤖 Google Sheet Expense Agent - CLI Mode")
    logger.info("=" * 60)
    
    try:
        result = run_agent_sync()
        
        logger.info("=" * 60)
        logger.info("✅ Agent finished successfully!")
        logger.info("=" * 60)
        
        if isinstance(result, dict):
            logger.info("📊 Results:")
            for key, value in result.items():
                logger.info(f"  {key}: {value}")
        else:
            logger.info(f"Result: {result}")
        
    except Exception as e:
        logger.error(f"❌ Agent failed: {e}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
