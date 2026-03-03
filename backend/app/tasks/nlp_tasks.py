from app.tasks.celery_app import app
from loguru import logger

@app.task(name="app.tasks.nlp_tasks.post_process_article")
def post_process_article(article_id: str):
    logger.info(f"Post-processing article: {article_id}")
    # Integration with sentiment, embedding, and digest generation will be in Phase 2
    logger.info(f"Phase 1 stub: Post-processing completed for {article_id}")
