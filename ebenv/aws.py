from __future__ import annotations

from typing import Literal

import boto3
import boto3.session
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig

# Configuration
########################################################################################

AWS_REGION = "ap-northeast-1"

# Exceptions
########################################################################################


class NoSecretKeyRetrieved(Exception):
    pass


# Helpers
########################################################################################


def get_django_secret_key(
    secret_id: str, version_stage: Literal["AWSCURRENT", "AWSPREVIOUS"]
) -> str:
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    cache_config = SecretCacheConfig()
    cache = SecretCache(config=cache_config, client=client)

    # returns secret string or None
    secret = cache.get_secret_string(secret_id, version_stage)

    if secret is None:
        raise NoSecretKeyRetrieved(
            f"No secret key retrieved. secret_id: {secret_id}, version_stage: {version_stage}"
        )

    return secret


def get_memcached_endpoints(cache_cluster_id: str) -> list[str]:
    """
    文字列の配列でキャッシュクラスターの各エンドポイントを返す
    """
    client = boto3.client("elasticache", region_name=AWS_REGION)

    response = client.describe_cache_clusters(
        CacheClusterId=cache_cluster_id,
        MaxRecords=20,
        ShowCacheNodeInfo=True,
    )
    cache_cluster = response["CacheClusters"][0]
    cache_nodes = cache_cluster["CacheNodes"]
    endpoints = [
        node["Endpoint"]["Address"] + ":" + str(node["Endpoint"]["Port"])
        for node in cache_nodes
    ]
    return endpoints
