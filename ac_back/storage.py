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

    def _get_resource_type(self, name):
        normalized_name = str(name).lower()

        # Vestnik latest issue PDFs must stay in raw to keep expected delivery URL.
        if normalized_name.endswith(".pdf") and normalized_name.startswith("journal/latest/"):
            return "raw"

        # Cloudinary may enforce lower limits for raw resources.
        # Store PDFs as image resources to allow larger file uploads.
        if normalized_name.endswith(".pdf"):
            return "image"
        return super()._get_resource_type(name)

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

        # Always use chunked upload for raw files to avoid 10 MB single-request limits.
        options["chunk_size"] = self.LARGE_UPLOAD_CHUNK_SIZE
        return cloudinary.uploader.upload_large(content, **options)
