# Autor: Daniel Aguado
# Fecha: 28/08/2017
# Desde: Lima - Peru

# -*- coding: utf-8 -*-

import arcpy
import os

arcpy.env.overwriteOutut = True

class mxd2other:
	def __init__(self):
		self.dir = arcpy.GetParameterAsText(0)
		self.format = arcpy.GetParameterAsText(1)
		self.dpi = arcpy.GetParameterAsText(2)
		self.quality = arcpy.GetParameterAsText(3)
		self.funtExport = {"PNG": arcpy.mapping.ExportToPNG, "JPEG": arcpy.mapping.ExportToJPEG, "TIFF": arcpy.mapping.ExportToTIFF}
		self.extention = {"PNG": ".PNG", "JPEG": ".jpg", "TIFF": ".tif", "PDF": ".pdf"}


	def export(self):
		if self.format == "PDF":
			arcpy.mapping.ExportToPDF(self.mxd, self.pathOut, "PAGE_LAYOUT", resolution=self.dpi, image_quality=self.quality)
		else:
			m = self.funtExport[self.format]
			m(self.mxd, self.pathOut, "PAGE_LAYOUT", resolution=self.dpi)


	def process(self):
		for p, f, x in os.walk(self.dir):
			for m in x:
				if m.split(".")[-1] == "mxd":
					try:
						name = "{}{}".format(m.split(".")[0], self.extention[self.format])
						pathMxd = os.path.join(p, m)
						self.pathOut = os.path.join(p, name)
						self.mxd = arcpy.mapping.MapDocument(pathMxd)
						self.export()
					except Exception as e:
						arcpy.AddWarning("\n {} \n".format(e))


	def main(self):
		self.process()


if __name__ == "__main__":
	obj = mxd2other()
	obj.main()
