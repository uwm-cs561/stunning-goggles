
DATA_FILE_NAME="bugswarm-data-$$(date +%Y-%m-%d_%H-%M-%S).tar.gz"

pack-data:
	@echo "Packing data..."
	@tar -czf $(DATA_FILE_NAME) data
	@echo "Data packed to $(DATA_FILE_NAME)."
	@mv $(DATA_FILE_NAME) ../../data/bugswarm/snapshot