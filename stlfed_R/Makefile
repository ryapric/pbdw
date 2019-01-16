R = R --vanilla CMD


all: build check install clean

FORCE:

build: FORCE
	$(R) build .

check: build
	$(R) check --no-manual *.tar.gz

test: FORCE
	Rscript -e 'devtools::test()'

define devtools_check
	Rscript -e " \
		tryCatch( \
			invisible(packageVersion('devtools')), \
			error = function(e) { \
				install.packages('devtools', repos = 'https://cloud.r-project.org') \
			} \
		)"
endef
install: FORCE
	@$(devtools_check); \
	Rscript -e 'devtools::install()'

install_src: FORCE
	$(R) INSTALL .

report: FORCE
	@Rscript -e 'rmarkdown::render(file.path(here::here(), "./inst/reports/forecast-report.Rmd"))'
	@Rscript -e 'file.copy(file.path(here::here(), "./inst/reports/forecast-report.html"), file.path(here::here(), "forecast-report.html"))'
	@xdg-open forecast-report.html

clean:
	rm -rf *.tar.gz *.Rcheck ..Rcheck
