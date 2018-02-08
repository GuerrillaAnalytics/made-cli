import boto3


class S3Wrapper():
    """
    Convenience wrapper around S3. Tailored to managing S3 structures using
    Guerrilla Analytics conventions
    """

    def truncate_key(self, object_key, depth):
        """
        Based on
        https://stackoverflow.com/questions/17060039/
        split-string-at-nth-occurrence-of-a-given-character
        """
        split_key = str(object_key).split('/')

        # Now join the split string back up to a specific depth
        truncated_key = '/'.join(split_key[:depth]) + '/'
        return truncated_key

    def getBucket(self):
        """Get a reference to the Bucket resource"""
        dev = boto3.session.Session(profile_name=self.profile_name)
        s3_resources = dev.resource('s3')
        bucket = s3_resources.Bucket(self.bucket_name)
        return bucket

    def __init__(self, bucket_name, profile_name=""):
        self.bucket_name = bucket_name
        self.profile_name = profile_name

        pass

    def listBucketContents(self, prefix_filter=""):
        """Create a list of all files and folders under
        a project
        """
        return self.getBucket().objects.filter(Prefix=prefix_filter)

    def listFolders(self, parent_key):
        all_keys = self.getBucket().objects \
            .filter(Prefix=parent_key)

        stop_at = parent_key.count('/') + 1
        print('Folder parent key:' + parent_key)
        print('stop-at' + str(stop_at))
        unique_versions = list(set({self.truncate_key(obj.key, stop_at) for obj in all_keys}))
        unique_versions.sort()

        return unique_versions


if __name__ == "__main__":
    # 'js-dpp-lab-ds1-data-dev'
    s3 = S3Wrapper('js-dpp-lab-ds1-data-dev', 'dpp1')
    print(s3.getBucket().name)
    # for obj in s3.getBucket().objects.filter(Prefix='projects/datalab_testing/'):
    #     print('{0}:{1}'.format(s3.getBucket().name, obj.key))

    contents = s3.listBucketContents(prefix_filter='projects/datalab_testing/')
    for obj in contents:
        print('{0}:{1}'.format(s3.getBucket().name, obj.key))

    print("All inputs")
    folders = s3.listFolders(parent_key='projects/ds044_depot_optimisation/inputs/')
    for key in folders:
        print('{0}:{1}'.format(s3.getBucket().name, key))
