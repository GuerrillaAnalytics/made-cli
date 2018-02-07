import boto3
import logging


class S3Wrapper():
    """
    Convenience wrapper around S3. Tailored to managing S3 structures using
    Guerrilla Analytics conventions
    """

    def getLastItemInKey(self, key):
        """
        Assumes key ends with / which is fairly safe with
        S3 keys retrieved from boto3
        """
        return key.rsplit('/', 2)[1]

    def truncate_key(self, object_key, depth):
        """
        based on
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

    def listInputs(self, project_name):
        """Create a list of keys of just the input folders in a project"""
        all_inputs = self.getBucket().objects \
            .filter(Prefix="projects/" + project_name + '/inputs/')

        unique_inputs = list(set({self.truncate_key(obj.key, 4) for obj in all_inputs}))
        unique_inputs.sort()

        return unique_inputs

    def listInputVersions(self, project_name, input_source):
        """Create a list of keys of just the input versions within a given source"""

        prefix_path = "projects/" + project_name + '/inputs/' + input_source + '/'
        print("Prefix path: " + prefix_path)
        all_inputs = self.getBucket().objects \
            .filter(Prefix=prefix_path)

        unique_versions = list(set({self.truncate_key(obj.key, 5) for obj in all_inputs}))
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

    print("List inputs:")
    inputs = s3.listInputs('ds044_depot_optimisation')
    for obj in inputs:
        print('{0}:{1}'.format(s3.getBucket().name, obj))

    source = s3.getLastItemInKey(inputs[2])
    print("Versions for: " + source)
    versions = s3.listInputVersions('ds044_depot_optimisation', source)
    for obj in versions:
         print('{0}:{1}'.format(s3.getBucket().name, obj))
