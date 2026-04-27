"""
pinecone_connector.py - MCP tool for semantic search against a Pinecone index.

This connector targets an index with an integrated embedding model
(llama-text-embed-v2, 1024 dimensions). No external embedding service needed.

Required environment variables:
    PINECONE_API_KEY   - Your Pinecone API key.
    PINECONE_INDEX     - Name of the index to query (e.g. "aiagent").

Optional:
    PINECONE_NAMESPACE - Namespace inside the index (defaults to empty string).
"""
import json
import os

from src.utils.logging_config import logger


def _get_index():
    from pinecone import Pinecone

    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise EnvironmentError("PINECONE_API_KEY is not set.")

    index_name = os.getenv("PINECONE_INDEX")
    if not index_name:
        raise EnvironmentError("PINECONE_INDEX is not set.")

    pc = Pinecone(api_key=api_key)
    return pc.Index(index_name)


def register(mcp):

    @mcp.tool()
    def query_pinecone(text: str, top_k: int = 5) -> str:
        """
        Run a semantic search against the Pinecone index using plain text.

        The index uses an integrated embedding model (llama-text-embed-v2),
        so no external embedding service is required. The text is embedded
        automatically by Pinecone at query time.

        Args:
            text:  Natural language query string.
            top_k: Number of nearest neighbors to return. Defaults to 5.

        Returns:
            JSON string with a list of matches, each containing id, score,
            and metadata.
        """
        try:
            index = _get_index()
            namespace = os.getenv("PINECONE_NAMESPACE", "__default__")

            response = index.search(
                namespace=namespace,
                query={
                    "inputs": {"text": text},
                    "top_k": top_k,
                },
                fields=["text", "category", "source"],
            )

            matches = []
            for hit in response.get("result", {}).get("hits", []):
                matches.append({
                    "id": hit.get("_id"),
                    "score": hit.get("_score"),
                    "fields": hit.get("fields", {}),
                })

            logger.info(
                "Pinecone query returned %d matches from index '%s'.",
                len(matches),
                os.getenv("PINECONE_INDEX"),
            )
            return json.dumps(matches, indent=2)

        except EnvironmentError as exc:
            logger.error("Configuration error: %s", exc)
            return f"Configuration error: {exc}"
        except Exception as exc:
            logger.error("Pinecone query failed: %s", exc)
            return f"Pinecone error: {exc}"

    @mcp.tool()
    def describe_pinecone_index() -> str:
        """
        Return metadata about the configured Pinecone index.

        Returns:
            JSON string with index name, dimension, metric, and status.
        """
        try:
            from pinecone import Pinecone

            api_key = os.getenv("PINECONE_API_KEY")
            index_name = os.getenv("PINECONE_INDEX")

            if not api_key or not index_name:
                return "Configuration error: PINECONE_API_KEY or PINECONE_INDEX is not set."

            pc = Pinecone(api_key=api_key)
            indexes = pc.list_indexes()

            for idx in indexes:
                if idx["name"] == index_name:
                    info = {
                        "name": idx["name"],
                        "dimension": idx["dimension"],
                        "metric": idx["metric"],
                        "status": idx["status"]["state"],
                        "host": idx["host"],
                        "embed_model": idx.get("embed", {}).get("model"),
                    }
                    logger.info("Described index: %s", index_name)
                    return json.dumps(info, indent=2)

            return f"Index '{index_name}' not found."

        except Exception as exc:
            logger.error("Error describing index: %s", exc)
            return f"Error: {exc}"

    @mcp.tool()
    def upsert_pinecone(records: list[dict]) -> str:
        """
        Insert or update records in the Pinecone index.

        The index uses an integrated embedding model, so text is embedded
        automatically. Do not pass vectors manually.

        Args:
            records: List of dicts, each with:
                - id (str): Unique identifier for the record.
                - text (str): The text content to embed and store.
                - metadata (dict, optional): Any additional fields to store
                  alongside the vector (e.g. source, category, date).

        Returns:
            Confirmation string with the number of records upserted.
        """
        try:
            index = _get_index()
            namespace = os.getenv("PINECONE_NAMESPACE", "__default__")

            formatted = []
            for record in records:
                if "id" not in record or "text" not in record:
                    return "Each record must have 'id' and 'text' fields."

                entry = {
                    "_id": record["id"],
                    "text": record["text"],
                }
                if "metadata" in record and isinstance(record["metadata"], dict):
                    entry.update(record["metadata"])

                formatted.append(entry)

            index.upsert_records(namespace=namespace, records=formatted)

            logger.info("Upserted %d records into index '%s'.", len(formatted), os.getenv("PINECONE_INDEX"))
            return f"OK - {len(formatted)} record(s) upserted."

        except EnvironmentError as exc:
            logger.error("Configuration error: %s", exc)
            return f"Configuration error: {exc}"
        except Exception as exc:
            logger.error("Upsert failed: %s", exc)
            return f"Pinecone error: {exc}"