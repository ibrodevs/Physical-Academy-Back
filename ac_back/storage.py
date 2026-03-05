import os

from cloudinary_storage.storage import RawMediaCloudinaryStorage as BaseRawMediaCloudinaryStorage


class RawMediaCloudinaryStorage(BaseRawMediaCloudinaryStorage):
    """
    Cloudinary raw storage with chunked upload fallback for files > 10 MB.
    """

    MAX_SINGLE_UPLOAD_SIZE = int(
        os.getenv("CLOUDINARY_MAX_SINGLE_UPLOAD_SIZE", str(10 * 1024 * 1024))
    )
    LARGE_UPLOAD_CHUNK_SIZE = int(
        os.getenv("CLOUDINARY_LARGE_UPLOAD_CHUNK_SIZE", str(6 * 1024 * 1024))
    )

    def _upload(self, name, content):
        import cloudinary.uploader

        options = {
            "use_filename": True,
            "resource_type": self._get_resource_type(name),
            "tags": self.TAG,
        }
        folder = os.path.dirname(name)
        if folder:
            options["folder"] = folder

        if hasattr(content, "seek"):
            content.seek(0)

        size = getattr(content, "size", None)
        if size is None and hasattr(content, "tell") and hasattr(content, "seek"):
            try:
                current_pos = content.tell()
                content.seek(0, os.SEEK_END)
                size = content.tell()
                content.seek(current_pos)
            except Exception:
                size = None

        # Some Cloudinary setups reject single upload requests above ~10 MB.
        # upload_large sends the file in chunks and avoids this request-size limit.
        if size is None or size > self.MAX_SINGLE_UPLOAD_SIZE:
            options["chunk_size"] = self.LARGE_UPLOAD_CHUNK_SIZE
            return cloudinary.uploader.upload_large(content, **options)

        return cloudinary.uploader.upload(content, **options)
