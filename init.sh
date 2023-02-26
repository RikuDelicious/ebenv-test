#!/bin/bash
aws secretsmanager put-secret-value --secret-id eb/ebenv-test/secret-key-02 --secret-string "newsecretkey" --region "ap-northeast-1"