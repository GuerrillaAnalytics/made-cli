import boto3


class S3Wrapper():
    """
    Convenience wrapper around S3. Tailored to managing S3 structures using
    Guerrilla Analytics conventions
    """

    def getBucket(self):
        """Get a reference to the Bucket resource"""
        dev = boto3.session.Session(profile_name=self.profile_name)
        s3 = dev.resource('s3')
        bucket = s3.Bucket(self.bucket_name)
        return bucket

    def __init__(self, bucket_name, profile_name=""):
        self.bucket_name = bucket_name
        self.profile_name = profile_name

        pass

    def listBucketContents(self, prefix_filter=""):
        return s3.getBucket().objects.filter(Prefix=prefix_filter)


if __name__ == "__main__":

    # 'js-dpp-lab-ds1-data-dev'
    s3 = S3Wrapper('js-dpp-lab-ds1-data-dev', 'dpp1')
    print(s3.getBucket().name)
    # for obj in s3.getBucket().objects.filter(Prefix='projects/datalab_testing/'):
    #     print('{0}:{1}'.format(s3.getBucket().name, obj.key))

    contents = s3.listBucketContents(prefix_filter='projects/datalab_testing/')
    for obj in contents:
        print('{0}:{1}'.format(s3.getBucket().name, obj.key))
    pass
