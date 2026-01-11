"""
Main entry point for ByteBrief Agent
"""
import argparse
import sys
from pathlib import Path
from loguru import logger
import json

# Add src to path so we can import bytebrief
sys.path.append(str(Path(__file__).parent.parent))

from bytebrief.core.models import ClientConfig
from bytebrief.agent.orchestrator import AgentOrchestrator

def setup_logger():
    """Configure logging"""
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add("logs/bytebrief.log", rotation="10 MB", level="DEBUG")

def main():
    setup_logger()
    
    parser = argparse.ArgumentParser(description="ByteBrief News Scraping Agent")
    parser.add_argument("--client", type=str, help="Path to client config JSON file")
    parser.add_argument("--keywords", type=str, help="Comma-separated keywords to filter by")
    parser.add_argument("--sources", type=str, help="Comma-separated sources to scrape (bbc, cnn)")
    parser.add_argument("--format", type=str, default="json", choices=["json", "csv", "markdown"], help="Output format")
    parser.add_argument("--output", type=str, help="Output file path")
    
    args = parser.parse_args()
    
    # Build client config
    if args.client:
        try:
            with open(args.client, 'r') as f:
                client_data = json.load(f)
                client_config = ClientConfig.from_dict(client_data)
        except Exception as e:
            logger.error(f"Failed to load client config: {e}")
            return
    else:
        # Create config from CLI args
        client_config = ClientConfig(
            name="CLI User",
            keywords=args.keywords.split(',') if args.keywords else [],
            preferred_sources=args.sources.split(',') if args.sources else [],
            output_format=args.format
        )
    
    # Run agent
    orchestrator = AgentOrchestrator()
    result = orchestrator.run(client_config)
    
    # Handle output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(result))
        logger.info(f"Results saved to {output_path}")
    else:
        print(result)

if __name__ == "__main__":
    main()
