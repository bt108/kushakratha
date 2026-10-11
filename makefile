# Define the source and destination directories
SRC_DIR := $(shell pwd)/markdown
DST_DIR := $(shell pwd)/epub

# Define the file extensions
SRC_EXT := .md
DST_EXT := .epub

# Define the pattern for source files
SRC_FILES := $(wildcard $(SRC_DIR)/*.md)

# Define the pattern for destination files
DST_FILES := $(patsubst $(SRC_DIR)/%.md,$(DST_DIR)/%.epub,$(SRC_FILES))

# Define config files
CSS_FILE := ./config/epub.css
TEMPLATE_FILE := ./config/template.epub3
METADATA_FILE := ./config/metadata.yaml
FONT_FILES := './fonts/*.ttf'

# Default target
all: $(DST_FILES)

# Rule to convert Markdown files to EPUB files
$(DST_DIR)/%.epub: $(SRC_DIR)/%.md $(CSS_FILE) $(TEMPLATE_FILE) $(METADATA_FILE)
	@echo "Converting $(SRC_DIR)/$*.md to $(DST_DIR)/$*.epub"
	@mkdir -p $(DST_DIR)
	pandoc -t epub3 --css $(CSS_FILE) --template=$(TEMPLATE_FILE) -o $@ $(METADATA_FILE) $<
# --epub-embed-font=$(FONT_FILES)
# Clean up the EPUB files
clean:
	rm -f $(DST_FILES)

# Debug target to output all variables
debug:
	@echo "SRC_DIR = $(SRC_DIR)"
	@echo "DST_DIR = $(DST_DIR)"
	@echo "SRC_EXT = $(SRC_EXT)"
	@echo "DST_EXT = $(DST_EXT)"
	@echo "CSS_FILE = $(CSS_FILE)"
	@echo "Checking for files in $(SRC_DIR):"
	@ls -l $(SRC_DIR)
	@echo "Expanded SRC_FILES: $(SRC_FILES)"
	@echo "Expanded DST_FILES: $(DST_FILES)"
	@echo "Testing wildcard function:"
	@echo $(wildcard $(SRC_DIR)/*.md)
	@echo "Testing shell command:"
	@echo $(shell ls $(SRC_DIR)/*.md)

.PHONY: all clean debug
