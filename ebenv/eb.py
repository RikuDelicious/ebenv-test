from __future__ import annotations

import json
import urllib.request
from subprocess import PIPE, Popen

# Helpers
########################################################################################


def get_environment_properties() -> dict[str, str]:
    """
    environment propertiesをdictで取得する
    ElasticBeanstalkで構築した環境のEC2インスタンス内でのみ実行可能
    予め提供されている以下のスクリプトツールを利用する
    /opt/elasticbeanstalk/bin/get-config environment [ options ]

    Docs:
    https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms-scripts.html
    """
    return json.loads(
        Popen(
            ["/opt/elasticbeanstalk/bin/get-config", "environment"], stdout=PIPE
        ).communicate()[0]
    )


def get_ec2_private_ip() -> str:
    """
    EC2インスタンスのプライベートIPアドレスを取得する

    EC2インスタンス内から以下のAPIを利用する
    http://169.254.169.254/latest/meta-data/local-ipv4/

    Docs:
    https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html
    """
    with urllib.request.urlopen(
        "http://169.254.169.254/latest/meta-data/local-ipv4/"
    ) as res:
        ec2_instance_private_ip = res.read().decode("utf-8")
    return ec2_instance_private_ip
