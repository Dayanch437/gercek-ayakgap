from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import FieldFile
from imagekit import ImageSpec
from PIL import Image, UnidentifiedImageError
import os
import uuid
from django.core.files.uploadedfile import TemporaryUploadedFile


def upload_file(instance: TemporaryUploadedFile, filename: str) -> str:
    path = type(instance).__name__.lower()

    filename, ext = filename.rsplit(".", 1)
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join(path, filename)


class CompressedImageSpec(ImageSpec):
    format = "WEBP"
    options = {"quality": 75}


class CompressedImageFile(FieldFile):
    def save(self, name, content, save=True):
        try:

            path = (
                content.temporary_file_path()
                if hasattr(content, "temporary_file_path")
                else content.name
            )

            if not path:
                content.seek(0)
                source_file = CompressedImageSpec(source=content)
                return super().save(name, source_file.generate(), save)

            with open(path, "rb") as file:
                if not (file.name.endswith(".gif") or file.name.endswith(".svg")):
                    image = Image.open(file)
                    image_format = CompressedImageSpec.format

                    compressed_image = ContentFile(b"")
                    image.save(compressed_image, format=image_format, quality=75)

                    base_name, _ = os.path.splitext(name)
                    name = f"{base_name}.{image_format.lower()}"

                    return super().save(name, compressed_image, save)
        except UnidentifiedImageError:
            pass

        return super().save(name, content, save)


class CompressedMixin:
    attr_class = CompressedImageFile

    def __init__(self, upload_to=upload_file, **kwargs):
        super().__init__(upload_to=upload_to, **kwargs)


class CompressedFileField(CompressedMixin, models.FileField):
    pass


class CompressedImageField(CompressedMixin, models.ImageField):
    pass
