from dateutil import parser
from django.core.management.base import BaseCommand
from lxml import etree
from pykml import parser
from pykml.factory import nsmap


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open("/Users/jasonbenn/Downloads/The Neighborhood - with houses.kml") as f:
            doc = parser.parse(f)

        namespaces = {"ns": nsmap[None]}
        root = doc.getroot()
        folders = root.xpath(".//ns:Folder", namespaces=namespaces)
        for folder in folders:
            print(folder.name)
            if folder.name not in ["Centers of gravity", "Communities"]:
                continue

            placemarks = folder.xpath(".//ns:Placemark[.//ns:Point]", namespaces=namespaces)
            for placemark in placemarks:
                coordinates = str(placemark.Point.coordinates).strip().split(',')[:2]
                description = placemark.description if hasattr(placemark, "description") else None
                print(placemark.name, description, coordinates)
