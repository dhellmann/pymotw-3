# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = build
SOURCEDIR     = source
CSS           = $(SOURCEDIR)/_themes/pymotw/static/pymotw.css
DEPLOYHOST    = pymotw.com
DEPLOYDIR     = /home/douhel3shell/pymotw.com/3/
LOCAL_DEPLOYDIR = ~/Sites/pymotw.com/3

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(SOURCEDIR)

default:
	@echo "html     - sphinx HTML build"
	@echo "spelling - spell check"
	@echo "css      - style sheet update"
	@echo "sitemap  - google sitemap"
	@echo "deploy   - copy to production server"
	@echo "publish  - html, spelling, deploy, git push"
	@echo "test     - copy to local test server"
	@echo "clean    - remove build artifacts"
	@echo "flake8   - run flake8 against the source files"
	@echo "cog      - run cog over all source files"

.PHONEY: all
all: html spelling

.PHONEY: spelling
spelling:
	$(SPHINXBUILD) -b spelling $(ALLSPHINXOPTS) $(BUILDDIR)/spelling

.PHONEY: html
html: $(CSS) _html

.PHONEY: _html
_html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

.PHONEY: css
css: $(BUILDDIR)/html/_static/pymotw.css

$(BUILDDIR)/html/_static/pymotw.css: $(CSS)
	cp $< $@

%.css: %.less
	chmod 0644 $@
	lessc -x $< > $@
	chmod 0444 $@

.PHONEY: sitemap
sitemap:
	./bin/sitemap_gen.py --config=etc/sitemap_gen_config.xml --testing

.PHONEY: sitemap-announce
sitemap-announce:
	./bin/sitemap_gen.py --config=etc/sitemap_gen_config.xml

.PHONEY: deploy
deploy: sitemap
	rsync -a -v --progress $(BUILDDIR)/html/ $(DEPLOYHOST):$(DEPLOYDIR)
	$(MAKE) sitemap-announce

.PHONE: publish
publish: html spelling deploy
#	git push

.PHONEY: test
test:
	(sleep 2 && echo "Openning..." && open http://localhost:8080) &
	(cd $(BUILDDIR)/html && python -m http.server 8080)

.PHONEY: clean
clean:
	rm -rf $(BUILDDIR)/doctrees $(BUILDDIR)/html

.PHONEY: flake8
flake8:
	flake8 $(SOURCEDIR)

.PHONE: cog
cog:
	paver cog
