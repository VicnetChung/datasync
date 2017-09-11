# -*- coding: utf-8 -*-

import oss2
import sys

def OssDownload():
    accessKeyId=sys.argv[1]
    accessSecret=sys.argv[2]
    EndPoint=sys.argv[3]
    Bucket=sys.argv[4]
    RemoteFile=sys.argv[5]
    LocalFile=sys.argv[6]

    auth = oss2.Auth(accessKeyId, accessSecret)
    #endpoint = EndPoint
    bucket = oss2.Bucket(auth, EndPoint, Bucket)

    oss2.resumable_download(bucket, RemoteFile, LocalFile,
                          store=oss2.ResumableDownloadStore(root='/tmp'),
                          multiget_threshold=20 * 1024 * 1024,
                          part_size=10 * 1024 * 1024,
                          num_threads=3)