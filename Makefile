default:
	@echo "Nothing to do"

clean:
	@find . -name '*.pyc' -delete
	@find . -name '*.stl' -delete
	@find . -name '*.svg' -delete
	@find . -name '*~' -delete
	@find . -name '*.dxf' -delete