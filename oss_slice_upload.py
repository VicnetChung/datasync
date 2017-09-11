#!/usr/bin/env python
#coding=utf-8

import os
import oss2
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
import sys

def OssSliceUpload():
    accessKeyId=sys.argv[1]
    accessSecret = sys.argv[2]
    EndPoint = sys.argv[3]
    Bucket = sys.argv[4]
    RemoteFile = sys.argv[5]
    LocalFile = sys.argv[6]

    auth = oss2.Auth(accessKeyId, accessSecret)
    bucket = oss2.Bucket(auth, EndPoint, Bucket)

    key = RemoteFile
    filename = LocalFile
    total_size = os.path.getsize(filename)
    part_size = determine_part_size(total_size, preferred_size=100 * 1024)
    # 初始化分片
    upload_id = bucket.init_multipart_upload(key).upload_id
    parts = []
    # 逐个上传分片
    with open(filename, 'rb') as fileobj:
        part_number = 1
        offset = 0
        while offset < total_size:
            num_to_upload = min(part_size, total_size - offset)
            result = bucket.upload_part(key, upload_id, part_number,
                                        SizedFileAdapter(fileobj, num_to_upload))
            parts.append(PartInfo(part_number, result.etag))
            offset += num_to_upload
            part_number += 1
    # 完成分片上传
    bucket.complete_multipart_upload(key, upload_id, parts)
    # 验证一下
    with open(filename, 'rb') as fileobj:
        assert bucket.get_object(key).read() == fileobj.read()