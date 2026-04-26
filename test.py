"""Simple smoke test entrypoint."""

from src.bootstrap import get_knowledge_service


def main() -> None:
    stats = get_knowledge_service().get_stats()
    print(f"collection={stats.collection_name}")
    print(f"document_count={stats.document_count}")
    print(f"storage_path={stats.storage_path}")


if __name__ == "__main__":
    main()
