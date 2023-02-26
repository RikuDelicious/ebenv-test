import re

import botocore.exceptions
import pytest

from ebenv import aws


def test_get_django_secret_key_awscurrent_exists():
    result = aws.get_django_secret_key(
        secret_id="eb/ebenv-test/secret-key-01", version_stage="AWSCURRENT"
    )
    assert result == "yesthisisasecretkeybutwedontusethis"


def test_get_django_secret_key_awscurrent_id_not_exists():
    with pytest.raises(botocore.exceptions.ClientError):
        aws.get_django_secret_key(
            secret_id="eb/ebenv-test/secret-key-not-exists", version_stage="AWSCURRENT"
        )


def test_get_django_secret_key_awsprevious_exists():
    current = aws.get_django_secret_key(
        secret_id="eb/ebenv-test/secret-key-02", version_stage="AWSCURRENT"
    )
    previous = aws.get_django_secret_key(
        secret_id="eb/ebenv-test/secret-key-02", version_stage="AWSPREVIOUS"
    )
    assert current == "newsecretkey"
    assert previous == "oldsecretkey_updatethis"


def test_get_django_secret_key_awsprevious_not_exists():
    with pytest.raises(aws.NoSecretKeyRetrieved):
        aws.get_django_secret_key(
            secret_id="eb/ebenv-test/secret-key-01", version_stage="AWSPREVIOUS"
        )


def test_get_memcached_endpoints_exists():
    endpoints = aws.get_memcached_endpoints(
        cache_cluster_id="eb-ebenv-test-memcached-cachecluster"
    )
    endpoint_pattern = re.compile(
        r"eb-ebenv-test-memcached-cachecluster\..+\.cache.amazonaws\.com:11211"
    )

    assert len(endpoints) == 2
    for endpoint in endpoints:
        result = endpoint_pattern.fullmatch(endpoint)
        assert result is not None


def test_get_memcached_endpoints_id_not_exists():
    with pytest.raises(botocore.exceptions.ClientError):
        aws.get_memcached_endpoints(
            cache_cluster_id="eb-ebenv-test-memcached-cachecluster-not-exists"
        )
